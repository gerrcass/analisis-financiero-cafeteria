"""Motor de referencia del modelo financiero de Cafetería Aurora.

Implementa las fórmulas de ``docs/project-brief.md`` sobre el contrato de
supuestos ``data/model.json``. El resultado es determinista y se usa para
generar ``data/expected.json``, para comparar con el motor JavaScript y como
oráculo de la recalculación del libro.

Uso:
    python scripts/model.py --write
    python scripts/model.py --scenario base --summary
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "data" / "model.json"
SCHEMA_PATH = ROOT / "data" / "schema.json"
EXPECTED_PATH = ROOT / "data" / "expected.json"

SCENARIO_KEYS: tuple[str, ...] = ("pessimistic", "base", "optimistic")
SCENARIO_LABELS = {
    "pessimistic": "Pesimista",
    "base": "Base",
    "optimistic": "Optimista",
}
TOLERANCE = {"eur": 1.0, "pp": 0.1}
MARGIN_FIELDS = {
    "grossMargin",
    "ebitdaMargin",
    "netMargin",
    "safetyMargin",
}
OVERVIEW_FIELDS = (
    "revenue",
    "cogs",
    "grossProfit",
    "grossMargin",
    "personnel",
    "opex",
    "ebitda",
    "ebitdaMargin",
    "depreciation",
    "ebit",
    "interest",
    "ebt",
    "tax",
    "netIncome",
    "netMargin",
    "closingCash",
    "ticketsPerDay",
    "averageTicketNet",
    "averageTicketGross",
    "breakEvenEbitda",
    "breakEvenTotal",
    "safetyMargin",
    "dscr",
    "fcff",
    "fcfe",
    "cfo",
    "maintenanceCapex",
    "workingCapitalChange",
    "principal",
)


def _r2(value: float) -> float:
    """Redondea a dos decimales evitando el -0.0."""
    out = round(float(value), 2)
    return 0.0 if out == 0 else out


def _r4(value: float) -> float:
    """Cuatro decimales para ratios que se comparan en puntos porcentuales."""
    return round(float(value), 4)


def _money(value: float) -> float:
    return _r2(value)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_model(path: str | Path = MODEL_PATH) -> dict[str, Any]:
    """Carga el contrato y valida su forma y sus invariantes."""
    data = _load_json(Path(path))
    validate_contract(data)
    return data


def validate_contract(
    data: Mapping[str, Any], schema_path: str | Path = SCHEMA_PATH
) -> None:
    """Valida el JSON Schema y las reglas económicas del brief.

    El esquema protege tipos y rangos; las comprobaciones semánticas protegen
    las sumas y el orden de escenarios que un JSON Schema no puede expresar.
    """
    import jsonschema

    schema = _load_json(Path(schema_path))
    jsonschema.validate(instance=data, schema=schema)

    errors: list[str] = []
    calendar = data["calendar"]
    products = data["products"]
    staff = data["staff"]
    capex = data["capex"]
    financing = data["financing"]
    scenarios = data["scenarios"]

    mix_total = sum(float(p["mix"]) for p in products)
    season_total = sum(float(s) for s in calendar["seasonality"])
    days_total = sum(float(d) for d in calendar["openingDays"])
    capex_total = sum(float(c["amount"]) for c in capex["items"])
    uses = capex_total + financing["initialStock"] + financing["openingCash"]
    sources = financing["equity"] + financing["loanAmount"]

    if abs(mix_total - 1.0) > 1e-9:
        errors.append(f"El mix de producto debe sumar 100 % (suma {mix_total:.6f}).")
    if abs(season_total - 12.0) > 1e-9:
        errors.append(f"La estacionalidad debe sumar 12,00 (suma {season_total:.6f}).")
    if abs(days_total - 312.0) > 1e-9:
        errors.append(f"Los días operativos deben sumar 312 (suma {days_total:.6f}).")
    if abs(sources - uses) > 1e-6:
        errors.append(f"Fuentes ({sources}) y usos ({uses}) no cuadran.")
    if sum(float(r["fte"][0]) for r in staff["roles"]) <= 0:
        errors.append("El plan de personal debe tener al menos un FTE.")
    for item in capex["items"]:
        if float(item["lifeYears"]) <= 0:
            errors.append(f"Vida útil no válida en {item['name']}.")
    for product in products:
        net_price = product["pvp"] / (1 + product["vat"])
        adjusted_cost = product["unitCost"] / (1 - product["waste"])
        if adjusted_cost >= net_price:
            errors.append(f"{product['name']} tiene un coste ajustado mayor que su precio neto.")

    if tuple(data["scenarioOrder"]) != SCENARIO_KEYS:
        errors.append("scenarioOrder debe ser pessimistic, base, optimistic.")
    if set(scenarios) != set(SCENARIO_KEYS):
        errors.append("Faltan escenarios o sobran claves.")

    if not _scenario_ordering_ok(scenarios):
        errors.append(
            "El orden de escenarios no es coherente: demanda/precio deben crecer "
            "y los costes deben bajar de Pesimista a Optimista."
        )

    payment = loan_payment(financing["loanAmount"], financing["loanRate"], financing["loanMonths"])
    # La cuota del brief es 1.402,66 €; el chequeo protege cambios accidentales.
    if abs(payment - 1402.6564) > 0.01:
        errors.append(f"La cuota del préstamo no coincide con el brief ({payment:.2f}).")

    if errors:
        raise ValueError("\n".join(errors))


def _scenario_ordering_ok(scenarios: Mapping[str, Mapping[str, Any]]) -> bool:
    ascending = (
        "demandFactor",
        "demandGrowth",
        "priceGrowth",
        "marketingPct",
    )
    descending = (
        "productCostInflation",
        "personnelFactor",
        "rentFactor",
        "servicesInflation",
        "otherOpexFactor",
        "otherOpexGrowth",
    )
    pes, base, opt = (scenarios[key] for key in SCENARIO_KEYS)
    return all(pes[field] < base[field] < opt[field] for field in ascending) and all(
        pes[field] > base[field] > opt[field] for field in descending
    )


def loan_payment(principal: float, annual_rate: float, months: int) -> float:
    """Cuota francesa constante. PMT(tipo/12, meses, -principal)."""
    if months <= 0:
        raise ValueError("El plazo debe ser positivo.")
    monthly = annual_rate / 12
    if monthly == 0:
        return principal / months
    return principal * monthly / (1 - (1 + monthly) ** -months)


def amortization_schedule(principal: float, annual_rate: float, months: int) -> list[dict[str, float]]:
    """Calendario completo del préstamo, mes a mes."""
    payment = loan_payment(principal, annual_rate, months)
    monthly = annual_rate / 12
    balance = principal
    schedule: list[dict[str, float]] = []
    for month in range(1, months + 1):
        interest = balance * monthly
        principal_paid = min(payment - interest, balance)
        if balance <= 1e-9:
            principal_paid = 0.0
        balance = max(0.0, balance - principal_paid)
        schedule.append(
            {
                "month": month,
                "opening": balance + principal_paid,
                "interest": interest,
                "principal": principal_paid,
                "closing": balance,
                "payment": interest + principal_paid,
            }
        )
    return schedule


def product_economics(data: Mapping[str, Any]) -> list[dict[str, float]]:
    """Precio neto, coste ajustado y margen unitario del catálogo."""
    products: list[dict[str, float]] = []
    for product in data["products"]:
        net_price = float(product["pvp"]) / (1 + float(product["vat"]))
        adjusted_cost = float(product["unitCost"]) / (1 - float(product["waste"]))
        margin = net_price - adjusted_cost
        products.append(
            {
                "id": product["id"],
                "name": product["name"],
                "category": product["category"],
                "pvp": float(product["pvp"]),
                "vat": float(product["vat"]),
                "netPrice": net_price,
                "unitCost": float(product["unitCost"]),
                "mix": float(product["mix"]),
                "waste": float(product["waste"]),
                "adjustedCost": adjusted_cost,
                "unitMargin": margin,
                "marginPct": margin / net_price if net_price else 0.0,
            }
        )
    return products


def staff_costs(data: Mapping[str, Any]) -> list[float]:
    """Coste empresa por año: Σ(FTE × salario) × (1+SS) × (1+crecimiento)^(y-1)."""
    staff = data["staff"]
    security = float(staff["employerSocialSecurity"])
    growth = float(staff["salaryGrowth"])
    costs: list[float] = []
    for year_index in range(3):
        base = sum(
            float(role["grossSalary"]) * float(role["fte"][year_index])
            for role in staff["roles"]
        )
        costs.append(base * (1 + security) * (1 + growth) ** year_index)
    return costs


def staff_fte_totals(data: Mapping[str, Any]) -> list[float]:
    return [
        sum(float(role["fte"][year]) for role in data["staff"]["roles"])
        for year in range(3)
    ]


def capex_summary(data: Mapping[str, Any]) -> dict[str, Any]:
    items = []
    total = 0.0
    annual_depreciation = 0.0
    for item in data["capex"]["items"]:
        amount = float(item["amount"])
        life = float(item["lifeYears"])
        total += amount
        annual_depreciation += amount / life
        items.append(
            {
                "name": item["name"],
                "amount": amount,
                "lifeYears": life,
                "annualDepreciation": amount / life,
                "monthlyDepreciation": amount / life / 12,
            }
        )
    return {
        "items": items,
        "total": total,
        "annualDepreciation": annual_depreciation,
        "monthlyDepreciation": annual_depreciation / 12,
    }


def _tax_bag(annual_ebt: Iterable[float], rate: float) -> dict[str, list[float]]:
    """Calcula cuota anual con una bolsa de pérdidas compensables."""
    losses = 0.0
    taxes: list[float] = []
    losses_start: list[float] = []
    taxable: list[float] = []
    losses_end: list[float] = []
    for result in annual_ebt:
        losses_start.append(losses)
        base = max(0.0, float(result) - losses)
        taxable.append(base)
        taxes.append(base * rate)
        losses = losses - min(losses, max(0.0, float(result))) + max(0.0, -float(result))
        losses_end.append(losses)
    return {
        "tax": taxes,
        "lossesStart": losses_start,
        "taxable": taxable,
        "lossesEnd": losses_end,
    }


def resolve_scenario(
    data: Mapping[str, Any], scenario_key: str, overrides: Mapping[str, float] | None = None
) -> dict[str, float | str]:
    """Devuelve los diez parámetros del escenario, con overrides opcionales.

    El laboratorio del sitio usa exactamente esta misma semántica: un override
    reemplaza el valor del escenario, nunca el contrato fuente.
    """
    if scenario_key not in data["scenarios"]:
        raise KeyError(f"Escenario desconocido: {scenario_key}")
    scenario = dict(data["scenarios"][scenario_key])
    allowed = {
        "demandFactor",
        "demandGrowth",
        "priceGrowth",
        "productCostInflation",
        "personnelFactor",
        "rentFactor",
        "servicesInflation",
        "marketingPct",
        "otherOpexFactor",
        "otherOpexGrowth",
    }
    if overrides:
        for key, value in overrides.items():
            if key not in allowed:
                raise KeyError(f"Override no permitido: {key}")
            scenario[key] = float(value)
    return scenario


def build_model(
    data: Mapping[str, Any],
    scenario_key: str = "base",
    overrides: Mapping[str, float] | None = None,
    modifiers: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Proyecta 36 meses y devuelve mensual, anual, deuda e indicadores.

    ``overrides`` reemplaza las diez variables del escenario (lo usa el
    laboratorio). ``modifiers`` aplica niveles de precio o coste para el
    análisis de sensibilidad documentado; no forma parte de la matriz.
    """
    scenario = resolve_scenario(data, scenario_key, overrides)
    modifiers = modifiers or {}
    price_level = float(modifiers.get("priceLevel", 1.0))
    cost_level = float(modifiers.get("costLevel", 1.0))

    calendar = data["calendar"]
    products = product_economics(data)
    weighted_net_price = sum(p["netPrice"] * p["mix"] for p in products)
    weighted_cost = sum(p["adjustedCost"] * p["mix"] for p in products)
    staff_by_year = staff_costs(data)
    capex = capex_summary(data)
    financing = data["financing"]
    loan = amortization_schedule(
        float(financing["loanAmount"]),
        float(financing["loanRate"]),
        int(financing["loanMonths"]),
    )
    loan_by_month = {entry["month"]: entry for entry in loan}
    tax_rate = float(data["tax"]["corporateRate"])
    wc_days = (
        float(data["workingCapital"]["inventoryDays"])
        - float(data["workingCapital"]["payableDays"])
        + float(data["workingCapital"]["receivableDays"])
    )

    months: list[dict[str, Any]] = []
    for index in range(36):
        month_number = index + 1
        year_index = index // 12
        calendar_month = index % 12
        days = float(calendar["openingDays"][calendar_month])
        tickets_per_day = (
            float(calendar["baseTicketsPerDay"])
            * float(scenario["demandFactor"])
            * (1 + float(scenario["demandGrowth"])) ** year_index
            * float(calendar["seasonality"][calendar_month])
            * (float(calendar["ramp"][calendar_month]) if year_index == 0 else 1.0)
        )
        tickets = tickets_per_day * days
        items = tickets * float(calendar["itemsPerTicket"])
        revenue = (
            items
            * weighted_net_price
            * (1 + float(scenario["priceGrowth"])) ** year_index
            * price_level
        )
        cogs = (
            items
            * weighted_cost
            * (1 + float(scenario["productCostInflation"])) ** year_index
            * cost_level
        )
        gross_profit = revenue - cogs
        personnel = staff_by_year[year_index] * float(scenario["personnelFactor"]) / 12
        rent = (
            float(data["fixedCosts"]["rent"])
            * float(scenario["rentFactor"])
            * (1 + float(data["fixedCosts"]["rentGrowth"])) ** year_index
        )
        utilities = float(data["fixedCosts"]["utilities"]) * (
            1 + float(scenario["servicesInflation"])
        ) ** year_index
        fixed_services = float(data["fixedCosts"]["fixedServices"]) * (
            1 + float(scenario["servicesInflation"])
        ) ** year_index
        fixed_marketing = float(data["fixedCosts"]["fixedMarketing"]) * (
            1 + float(data["fixedCosts"]["fixedMarketingGrowth"])
        ) ** year_index
        variable_marketing = float(scenario["marketingPct"]) * revenue
        other_opex = (
            float(data["fixedCosts"]["other"])
            * float(scenario["otherOpexFactor"])
            * (1 + float(scenario["otherOpexGrowth"])) ** year_index
        )
        total_opex = (
            personnel
            + rent
            + utilities
            + fixed_services
            + fixed_marketing
            + variable_marketing
            + other_opex
        )
        ebitda = gross_profit - total_opex
        depreciation = capex["monthlyDepreciation"]
        ebit = ebitda - depreciation
        debt = loan_by_month[month_number]
        interest = debt["interest"]
        principal = debt["principal"]
        ebt = ebit - interest
        working_capital = cogs * wc_days / 365
        months.append(
            {
                "index": index + 1,
                "month": month_number,
                "year": int(calendar["years"][year_index]),
                "yearIndex": year_index,
                "calendarMonth": calendar_month + 1,
                "monthLabel": _month_label(calendar_month + 1),
                "openingDays": days,
                "ticketsPerDay": tickets_per_day,
                "tickets": tickets,
                "items": items,
                "revenue": revenue,
                "cogs": cogs,
                "grossProfit": gross_profit,
                "personnel": personnel,
                "rent": rent,
                "utilities": utilities,
                "fixedServices": fixed_services,
                "fixedMarketing": fixed_marketing,
                "variableMarketing": variable_marketing,
                "otherOpex": other_opex,
                "totalOpex": total_opex,
                "ebitda": ebitda,
                "depreciation": depreciation,
                "ebit": ebit,
                "interest": interest,
                "ebt": ebt,
                "debtOpening": debt["opening"],
                "debtClosing": debt["closing"],
                "principal": principal,
                "workingCapital": working_capital,
                "maintenanceCapex": 0.0,
                "tax": 0.0,
                "netIncome": 0.0,
                "taxNoDebt": 0.0,
                "taxShield": 0.0,
                "fcff": 0.0,
                "fcfe": 0.0,
                "openingCash": 0.0,
                "closingCash": 0.0,
                "dscr": 0.0,
            }
        )

    annual_ebt = [sum(m["ebt"] for m in months[y * 12 : (y + 1) * 12]) for y in range(3)]
    annual_ebit = [sum(m["ebit"] for m in months[y * 12 : (y + 1) * 12]) for y in range(3)]
    tax_with_debt = _tax_bag(annual_ebt, tax_rate)
    tax_without_debt = _tax_bag(annual_ebit, tax_rate)

    initial_stock = float(financing["initialStock"])
    for index, month in enumerate(months):
        year_index = index // 12
        statement_tax = tax_with_debt["tax"][year_index] / 12
        theoretical_tax = tax_without_debt["tax"][year_index] / 12
        month["tax"] = statement_tax
        month["netIncome"] = month["ebt"] - statement_tax
        month["taxNoDebt"] = theoretical_tax
        month["taxShield"] = theoretical_tax - statement_tax
        month["maintenanceCapex"] = month["revenue"] * float(data["capex"]["maintenancePct"])
        previous_wc = initial_stock if index == 0 else months[index - 1]["workingCapital"]
        month["workingCapitalChange"] = month["workingCapital"] - previous_wc
        month["fcff"] = (
            month["ebitda"]
            - month["taxNoDebt"]
            - month["maintenanceCapex"]
            - month["workingCapitalChange"]
        )
        month["fcfe"] = (
            month["fcff"]
            - month["interest"]
            + month["taxShield"]
            - month["principal"]
        )
        month["openingCash"] = (
            float(financing["openingCash"]) if index == 0 else months[index - 1]["closingCash"]
        )
        month["closingCash"] = month["openingCash"] + month["fcfe"]
        month["dscr"] = (
            (month["ebitda"] - month["tax"]) / (month["interest"] + month["principal"])
            if month["interest"] + month["principal"]
            else 0.0
        )
        month["grossMargin"] = month["grossProfit"] / month["revenue"] if month["revenue"] else 0.0
        month["ebitdaMargin"] = month["ebitda"] / month["revenue"] if month["revenue"] else 0.0
        month["netMargin"] = month["netIncome"] / month["revenue"] if month["revenue"] else 0.0

    annual: dict[str, dict[str, Any]] = {}
    for year_index, year in enumerate(calendar["years"]):
        slice_ = months[year_index * 12 : (year_index + 1) * 12]
        revenue = sum(m["revenue"] for m in slice_)
        cogs = sum(m["cogs"] for m in slice_)
        gross_profit = revenue - cogs
        personnel = sum(m["personnel"] for m in slice_)
        opex = sum(m["totalOpex"] - m["personnel"] for m in slice_)
        ebitda = gross_profit - personnel - opex
        depreciation = sum(m["depreciation"] for m in slice_)
        ebit = ebitda - depreciation
        interest = sum(m["interest"] for m in slice_)
        ebt = ebit - interest
        tax = tax_with_debt["tax"][year_index]
        net_income = ebt - tax
        tickets = sum(m["tickets"] for m in slice_)
        days = sum(m["openingDays"] for m in slice_)
        tickets_per_day = tickets / days
        fixed_cash_costs = (
            personnel
            + sum(m["rent"] for m in slice_)
            + sum(m["utilities"] for m in slice_)
            + sum(m["fixedServices"] for m in slice_)
            + sum(m["fixedMarketing"] for m in slice_)
            + sum(m["otherOpex"] for m in slice_)
        )
        variable_marketing = sum(m["variableMarketing"] for m in slice_)
        contribution_per_ticket = (revenue - cogs - variable_marketing) / tickets
        break_even_ebitda = fixed_cash_costs / contribution_per_ticket / days
        break_even_total = (
            fixed_cash_costs + depreciation + interest
        ) / contribution_per_ticket / days
        safety_margin = (tickets_per_day - break_even_total) / tickets_per_day
        dscr = (ebitda - tax) / (interest + sum(m["principal"] for m in slice_))
        closing_cash = slice_[-1]["closingCash"]
        fcfe = sum(m["fcfe"] for m in slice_)
        fcff = sum(m["fcff"] for m in slice_)
        cfo = net_income + depreciation - sum(m["workingCapitalChange"] for m in slice_)

        annual[str(year)] = {
            "year": int(year),
            "openingCash": slice_[0]["openingCash"],
            "closingCash": closing_cash,
            "revenue": revenue,
            "cogs": cogs,
            "grossProfit": gross_profit,
            "grossMargin": gross_profit / revenue if revenue else 0.0,
            "personnel": personnel,
            "personnelPct": personnel / revenue if revenue else 0.0,
            "opex": opex,
            "totalOpex": personnel + opex,
            "ebitda": ebitda,
            "ebitdaMargin": ebitda / revenue if revenue else 0.0,
            "depreciation": depreciation,
            "ebit": ebit,
            "ebitMargin": ebit / revenue if revenue else 0.0,
            "interest": interest,
            "ebt": ebt,
            "tax": tax,
            "taxable": tax_with_debt["taxable"][year_index],
            "taxLossesStart": tax_with_debt["lossesStart"][year_index],
            "taxLossesEnd": tax_with_debt["lossesEnd"][year_index],
            "netIncome": net_income,
            "netMargin": net_income / revenue if revenue else 0.0,
            "tickets": tickets,
            "ticketsPerDay": tickets_per_day,
            "averageTicketNet": revenue / tickets if tickets else 0.0,
            "averageTicketGross": revenue / tickets * (1 + float(calendar["vat"])) if tickets else 0.0,
            "breakEvenEbitda": break_even_ebitda,
            "breakEvenTotal": break_even_total,
            "safetyMargin": safety_margin,
            "contributionPerTicket": contribution_per_ticket,
            "fixedCashCosts": fixed_cash_costs,
            "dscr": dscr,
            "principal": sum(m["principal"] for m in slice_),
            "fcff": fcff,
            "fcfe": fcfe,
            "cfo": cfo,
            "maintenanceCapex": sum(m["maintenanceCapex"] for m in slice_),
            "workingCapitalChange": sum(m["workingCapitalChange"] for m in slice_),
            "taxNoDebt": tax_without_debt["tax"][year_index],
            "taxShield": tax_without_debt["tax"][year_index] - tax,
            "debtClosing": slice_[-1]["debtClosing"],
        }

    product_profitability = []
    for year_index, year in enumerate(calendar["years"]):
        block = []
        for product in products:
            units = sum(m["items"] for m in months[year_index * 12 : (year_index + 1) * 12]) * product["mix"]
            revenue = units * product["netPrice"] * (1 + float(scenario["priceGrowth"])) ** year_index * price_level
            cogs = (
                units
                * product["adjustedCost"]
                * (1 + float(scenario["productCostInflation"])) ** year_index
                * cost_level
            )
            gross = revenue - cogs
            block.append(
                {
                    "id": product["id"],
                    "name": product["name"],
                    "units": units,
                    "revenue": revenue,
                    "cogs": cogs,
                    "grossProfit": gross,
                    "marginPct": gross / revenue if revenue else 0.0,
                }
            )
        product_profitability.append({"year": int(year), "products": block})

    cumulative_fcff = 0.0
    cumulative_fcfe = 0.0
    payback_project = None
    payback_equity = None
    project_target = capex["total"] + initial_stock
    for month in months:
        cumulative_fcff += month["fcff"]
        cumulative_fcfe += month["fcfe"]
        if payback_project is None and cumulative_fcff >= project_target:
            payback_project = month["month"]
        if payback_equity is None and cumulative_fcfe >= float(financing["equity"]):
            payback_equity = month["month"]

    loan_end = loan[-1]["closing"] if loan else 0.0
    checks = {
        "grossMarginIdentity": max(
            abs(m["grossProfit"] - (m["revenue"] - m["cogs"])) for m in months
        ),
        "ebitdaIdentity": max(
            abs(m["ebitda"] - (m["grossProfit"] - m["totalOpex"])) for m in months
        ),
        "ebitIdentity": max(abs(m["ebit"] - (m["ebitda"] - m["depreciation"])) for m in months),
        "ebtIdentity": max(abs(m["ebt"] - (m["ebit"] - m["interest"])) for m in months),
        "netIncomeIdentity": max(abs(m["netIncome"] - (m["ebt"] - m["tax"])) for m in months),
        "cashIdentity": max(
            abs(m["closingCash"] - (m["openingCash"] + m["fcfe"])) for m in months
        ),
        "fcfeIdentity": max(
            abs(
                m["fcfe"]
                - (
                    m["fcff"]
                    - m["interest"]
                    + m["taxShield"]
                    - m["principal"]
                )
            )
            for m in months
        ),
        "cashReconciliation": max(
            abs(
                m["fcfe"]
                - (
                    m["netIncome"]
                    + m["depreciation"]
                    - m["maintenanceCapex"]
                    - m["workingCapitalChange"]
                    - m["principal"]
                )
            )
            for m in months
        ),
        "loanClosesAtZero": round(loan_end, 6),
        "paybackProjectMonths": payback_project,
        "paybackEquityMonths": payback_equity,
        "minimumCash": min(m["closingCash"] for m in months),
        "annualSumRevenueDelta": abs(
            sum(a["revenue"] for a in annual.values()) - sum(m["revenue"] for m in months)
        ),
        "productRevenueDelta2028": abs(
            sum(p["revenue"] for p in product_profitability[-1]["products"]) - annual["2028"]["revenue"]
        ),
        "productCogsDelta2028": abs(
            sum(p["cogs"] for p in product_profitability[-1]["products"]) - annual["2028"]["cogs"]
        ),
    }

    return {
        "scenarioKey": scenario_key,
        "scenario": scenario,
        "products": products,
        "weightedNetPrice": weighted_net_price,
        "weightedCost": weighted_cost,
        "staffCostByYear": staff_by_year,
        "staffFteByYear": staff_fte_totals(data),
        "capex": capex,
        "loan": loan,
        "loanPayment": loan_by_month[1]["payment"],
        "months": months,
        "annual": annual,
        "productProfitability": product_profitability,
        "paybackProjectMonths": payback_project,
        "paybackEquityMonths": payback_equity,
        "cumulativeFcff": sum(m["fcff"] for m in months),
        "cumulativeFcfe": sum(m["fcfe"] for m in months),
        "cashOnCash": sum(m["fcfe"] for m in months) / float(financing["equity"]),
        "checks": checks,
    }


def _month_label(month: int) -> str:
    labels = (
        "ene",
        "feb",
        "mar",
        "abr",
        "may",
        "jun",
        "jul",
        "ago",
        "sep",
        "oct",
        "nov",
        "dic",
    )
    return labels[month - 1]


def expected_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    """Construye el JSON de objetivos dorados, redondeado y determinista."""
    scenarios: dict[str, Any] = {}
    for key in SCENARIO_KEYS:
        result = build_model(data, key)
        annual = {
            year: {
                field: (_r4(annual_row[field]) if field in MARGIN_FIELDS else _r2(annual_row[field]))
                for field in OVERVIEW_FIELDS
            }
            for year, annual_row in result["annual"].items()
        }
        product_profitability = []
        for block in result["productProfitability"]:
            product_profitability.append(
                {
                    "year": block["year"],
                    "products": [
                        {
                            "id": product["id"],
                            "name": product["name"],
                            "units": _r2(product["units"]),
                            "revenue": _r2(product["revenue"]),
                            "cogs": _r2(product["cogs"]),
                            "grossProfit": _r2(product["grossProfit"]),
                            "marginPct": _r2(product["marginPct"] * 100),
                        }
                        for product in block["products"]
                    ],
                }
            )
        scenarios[key] = {
            "name": SCENARIO_LABELS[key],
            "annual": annual,
            "paybackProjectMonths": result["paybackProjectMonths"],
            "paybackEquityMonths": result["paybackEquityMonths"],
            "cumulativeFcfe": _r2(result["cumulativeFcfe"]),
            "cumulativeFcff": _r2(result["cumulativeFcff"]),
            "cashOnCash": _r2(result["cashOnCash"] * 100),
            "minimumCash": _r2(result["checks"]["minimumCash"]),
            "loanClosesAtZero": _r2(result["checks"]["loanClosesAtZero"]),
            "productProfitability": product_profitability,
        }
    products = product_economics(data)
    capex = capex_summary(data)
    staff = staff_costs(data)
    contract = {
        "mixTotal": _r2(sum(p["mix"] for p in products) * 100),
        "seasonalityTotal": _r2(sum(data["calendar"]["seasonality"])),
        "openingDaysTotal": _r2(sum(data["calendar"]["openingDays"])),
        "weightedNetPrice": _r4(sum(p["netPrice"] * p["mix"] for p in products)),
        "weightedCost": _r4(sum(p["adjustedCost"] * p["mix"] for p in products)),
        "weightedGrossMargin": _r2(
            (1 - sum(p["adjustedCost"] * p["mix"] for p in products) / sum(p["netPrice"] * p["mix"] for p in products)) * 100
        ),
        "capexTotal": _r2(capex["total"]),
        "annualDepreciation": _r2(capex["annualDepreciation"]),
        "staffCostByYear": [_r2(v) for v in staff],
        "sources": _r2(data["financing"]["equity"] + data["financing"]["loanAmount"]),
        "uses": _r2(
            capex["total"] + data["financing"]["initialStock"] + data["financing"]["openingCash"]
        ),
        "loanPayment": _r2(loan_payment(
            data["financing"]["loanAmount"],
            data["financing"]["loanRate"],
            int(data["financing"]["loanMonths"]),
        )),
        "scenarioOrdering": True,
    }
    return {
        "meta": {
            "version": str(data["meta"]["version"]),
            "generatedAt": str(data["meta"]["generatedAt"]),
            "tolerance": TOLERANCE,
            "source": "data/model.json",
        },
        "contract": contract,
        "scenarios": scenarios,
    }


def write_expected(data: Mapping[str, Any], path: str | Path = EXPECTED_PATH) -> Path:
    payload = expected_payload(data)
    target = Path(path)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    return target


def _summary(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "scenario": SCENARIO_LABELS[result["scenarioKey"]],
        "annual": {
            year: {
                field: (_r4(row[field]) if field in MARGIN_FIELDS else _r2(row[field]))
                for field in OVERVIEW_FIELDS
            }
            for year, row in result["annual"].items()
        },
        "paybackProjectMonths": result["paybackProjectMonths"],
        "paybackEquityMonths": result["paybackEquityMonths"],
        "cumulativeFcfe": _r2(result["cumulativeFcfe"]),
        "cashOnCash": _r2(result["cashOnCash"] * 100),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Modelo financiero Cafetería Aurora")
    parser.add_argument("--input", default=str(MODEL_PATH), help="Contrato de supuestos")
    parser.add_argument("--output", default=str(EXPECTED_PATH), help="Objetivos dorados")
    parser.add_argument("--scenario", choices=SCENARIO_KEYS, default="base")
    parser.add_argument("--summary", action="store_true", help="Imprime un resumen legible")
    parser.add_argument("--write", action="store_true", help="Escribe data/expected.json")
    args = parser.parse_args(argv)

    data = load_model(args.input)
    if args.write:
        path = write_expected(data, args.output)
        print(f"Objetivos dorados escritos en {path}")
    if args.summary:
        result = build_model(data, args.scenario)
        print(json.dumps(_summary(result), ensure_ascii=False, indent=2))
    if not args.write and not args.summary:
        result = build_model(data, args.scenario)
        print(json.dumps(_summary(result), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
