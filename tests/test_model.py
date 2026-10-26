from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest

from scripts.model import (
    SCENARIO_KEYS,
    _tax_bag,
    amortization_schedule,
    build_model,
    capex_summary,
    expected_payload,
    load_model,
    loan_payment,
    product_economics,
    staff_costs,
    validate_contract,
    write_expected,
)
from scripts.model import MODEL_PATH, EXPECTED_PATH


@pytest.fixture(scope="module")
def contract():
    return load_model()


@pytest.fixture(scope="module")
def base(contract):
    return build_model(contract, "base")


def test_contract_sums_and_sources_match_the_brief(contract):
    products = product_economics(contract)
    assert sum(product["mix"] for product in products) == pytest.approx(1.0)
    assert sum(contract["calendar"]["seasonality"]) == pytest.approx(12.0)
    assert sum(contract["calendar"]["openingDays"]) == 312
    assert capex_summary(contract)["total"] == pytest.approx(132000)
    assert contract["financing"]["equity"] + contract["financing"]["loanAmount"] == pytest.approx(
        capex_summary(contract)["total"]
        + contract["financing"]["initialStock"]
        + contract["financing"]["openingCash"]
    )
    assert loan_payment(70000, 0.075, 60) == pytest.approx(1402.6564, abs=0.001)
    assert staff_costs(contract) == pytest.approx([110460, 129349.975, 133230.47425], abs=0.01)


def test_products_match_the_brief_table(contract):
    products = product_economics(contract)
    assert products[0]["name"] == "Espresso"
    assert products[0]["netPrice"] == pytest.approx(1.5455, abs=1e-4)
    assert products[0]["adjustedCost"] == pytest.approx(0.4375, abs=1e-4)
    assert products[0]["unitMargin"] == pytest.approx(1.108, abs=1e-4)
    assert products[5]["marginPct"] == pytest.approx(0.5738, abs=1e-3)
    weighted_price = sum(p["netPrice"] * p["mix"] for p in products)
    weighted_cost = sum(p["adjustedCost"] * p["mix"] for p in products)
    assert weighted_price == pytest.approx(2.6691, abs=1e-4)
    assert weighted_cost == pytest.approx(0.9207, abs=1e-4)
    assert 1 - weighted_cost / weighted_price == pytest.approx(0.6550, abs=1e-4)


def test_invalid_contracts_are_rejected(contract):
    broken = copy.deepcopy(contract)
    broken["products"][0]["mix"] += 0.01
    with pytest.raises(ValueError, match="mix"):
        validate_contract(broken)

    broken = copy.deepcopy(contract)
    broken["calendar"]["seasonality"][0] = 0.91
    with pytest.raises(ValueError, match="estacionalidad"):
        validate_contract(broken)

    broken = copy.deepcopy(contract)
    broken["calendar"]["openingDays"][0] = 28
    with pytest.raises(ValueError, match="días"):
        validate_contract(broken)

    broken = copy.deepcopy(contract)
    broken["scenarios"]["pessimistic"]["demandFactor"] = 1.04
    with pytest.raises(ValueError, match="orden"):
        validate_contract(broken)


def test_annual_golden_values_for_base(base):
    year = base["annual"]["2026"]
    assert year["revenue"] == pytest.approx(384418.75, abs=1)
    assert year["cogs"] == pytest.approx(132608.40, abs=1)
    assert year["grossProfit"] == pytest.approx(251810.36, abs=1)
    assert year["personnel"] == pytest.approx(110460.0, abs=1)
    assert year["opex"] == pytest.approx(79692.56, abs=1)
    assert year["ebitda"] == pytest.approx(61657.79, abs=1)
    assert year["depreciation"] == pytest.approx(16625.0, abs=1)
    assert year["ebit"] == pytest.approx(45032.79, abs=1)
    assert year["interest"] == pytest.approx(4843.46, abs=1)
    assert year["ebt"] == pytest.approx(40189.33, abs=1)
    assert year["tax"] == pytest.approx(10047.33, abs=1)
    assert year["netIncome"] == pytest.approx(30142.0, abs=1)
    assert year["closingCash"] == pytest.approx(57456.0, abs=1)
    assert year["ticketsPerDay"] == pytest.approx(341.94, abs=1)
    assert year["averageTicketNet"] == pytest.approx(3.602, abs=0.01)
    assert year["breakEvenEbitda"] == pytest.approx(254.20, abs=0.1)
    assert year["breakEvenTotal"] == pytest.approx(284.75, abs=0.1)
    assert year["safetyMargin"] == pytest.approx(0.1673, abs=0.001)
    assert year["dscr"] == pytest.approx(3.07, abs=0.01)

    assert base["annual"]["2028"]["revenue"] == pytest.approx(460863.67, abs=1)
    assert base["annual"]["2028"]["ebitda"] == pytest.approx(79505.07, abs=1)
    assert base["annual"]["2028"]["netIncome"] == pytest.approx(44977.69, abs=1)
    assert base["annual"]["2028"]["closingCash"] == pytest.approx(132062.61, abs=1)


def test_base_payback_and_return(base):
    assert base["paybackProjectMonths"] == 34
    assert base["paybackEquityMonths"] == 30
    assert base["cumulativeFcfe"] == pytest.approx(110562.61, abs=1)
    assert base["cashOnCash"] == pytest.approx(1.2285, abs=0.001)
    assert base["checks"]["loanClosesAtZero"] == pytest.approx(0.0, abs=0.01)
    assert base["annual"]["2028"]["debtClosing"] == pytest.approx(31170.42, abs=0.01)


def test_scenario_ordering_and_pessimistic_survival(contract):
    results = {key: build_model(contract, key) for key in SCENARIO_KEYS}
    assert results["pessimistic"]["annual"]["2028"]["revenue"] < results["base"]["annual"]["2028"]["revenue"]
    assert results["base"]["annual"]["2028"]["revenue"] < results["optimistic"]["annual"]["2028"]["revenue"]
    assert results["pessimistic"]["annual"]["2028"]["netIncome"] == pytest.approx(133.60, abs=1)
    assert results["pessimistic"]["annual"]["2028"]["dscr"] == pytest.approx(1.17, abs=0.01)
    assert results["pessimistic"]["paybackProjectMonths"] is None
    assert results["optimistic"]["paybackProjectMonths"] == 25
    assert results["optimistic"]["cumulativeFcfe"] == pytest.approx(178824.60, abs=1)


def test_monthly_identities(contract):
    for key in SCENARIO_KEYS:
        result = build_model(contract, key)
        assert result["checks"]["grossMarginIdentity"] < 1e-6
        assert result["checks"]["ebitdaIdentity"] < 1e-6
        assert result["checks"]["ebitIdentity"] < 1e-6
        assert result["checks"]["ebtIdentity"] < 1e-6
        assert result["checks"]["netIncomeIdentity"] < 1e-6
        assert result["checks"]["cashIdentity"] < 1e-6
        assert result["checks"]["fcfeIdentity"] < 1e-6
        assert result["checks"]["cashReconciliation"] < 1e-6
        assert result["checks"]["annualSumRevenueDelta"] < 1e-6
        assert result["checks"]["productRevenueDelta2028"] < 1e-6


def test_cash_reconciliation_against_net_income(base):
    for month in base["months"]:
        expected_fcfe = (
            month["netIncome"]
            + month["depreciation"]
            - month["maintenanceCapex"]
            - month["workingCapitalChange"]
            - month["principal"]
        )
        assert month["fcfe"] == pytest.approx(expected_fcfe, abs=1e-6)


def test_debt_schedule_uses_pmt_and_closes(contract):
    payment = loan_payment(70000, 0.075, 60)
    schedule = amortization_schedule(70000, 0.075, 60)
    assert len(schedule) == 60
    assert schedule[0]["interest"] == pytest.approx(437.5, abs=0.01)
    assert schedule[0]["principal"] == pytest.approx(965.1564, abs=0.01)
    assert schedule[-1]["closing"] == pytest.approx(0, abs=0.01)
    assert sum(item["payment"] for item in schedule) == pytest.approx(payment * 60, abs=0.01)
    assert sum(item["interest"] for item in schedule) == pytest.approx(14159.38, abs=0.5)


def test_tax_loss_bag_carries_losses_and_pays_zero():
    result = _tax_bag([-100.0, 50.0, 200.0], 0.25)
    assert result["tax"] == pytest.approx([0.0, 0.0, 37.5])
    assert result["lossesStart"] == pytest.approx([0.0, 100.0, 50.0])
    assert result["taxable"] == pytest.approx([0.0, 0.0, 150.0])
    assert result["lossesEnd"] == pytest.approx([100.0, 50.0, 0.0])


def test_synthetic_loss_scenario_has_zero_tax(contract):
    scenario = copy.deepcopy(contract)
    # Un factor de demanda muy bajo lleva a EBT negativo en 2026 y 2027.
    result = build_model(scenario, "base", {"demandFactor": 0.35, "personnelFactor": 1.15})
    assert result["annual"]["2026"]["ebt"] < 0
    assert result["annual"]["2027"]["ebt"] < 0
    assert result["annual"]["2026"]["tax"] == 0
    assert result["annual"]["2027"]["tax"] == 0
    assert result["annual"]["2027"]["taxLossesStart"] > 0


def test_documented_sensitivities(contract):
    base = build_model(contract, "base")
    ebitda = base["annual"]["2026"]["ebitda"]
    assert build_model(contract, "base", {"demandFactor": 0.9})["annual"]["2026"]["ebitda"] == pytest.approx(
        ebitda - 24027.79, abs=1
    )
    assert build_model(contract, "base", {"demandFactor": 1.1})["annual"]["2026"]["ebitda"] == pytest.approx(
        ebitda + 24027.79, abs=1
    )
    price = build_model(contract, "base", modifiers={"priceLevel": 1.05})
    assert price["annual"]["2026"]["ebitda"] == pytest.approx(ebitda + 18644.39, abs=1)
    personnel = build_model(contract, "base", {"personnelFactor": 1.05})
    assert personnel["annual"]["2026"]["ebitda"] == pytest.approx(ebitda - 5523, abs=1)
    rent = build_model(contract, "base", {"rentFactor": 1.1})
    assert rent["annual"]["2026"]["ebitda"] == pytest.approx(ebitda - 2280, abs=1)
    marketing = build_model(contract, "base", {"marketingPct": 0.04})
    assert marketing["annual"]["2026"]["ebitda"] == pytest.approx(ebitda - 3844.19, abs=1)
    cost = build_model(contract, "base", {"productCostInflation": 0.045})
    assert cost["annual"]["2026"]["ebitda"] == pytest.approx(ebitda, abs=0.5)
    assert cost["annual"]["2027"]["ebitda"] == pytest.approx(
        base["annual"]["2027"]["ebitda"] - 1455.0, abs=1
    )


def test_product_profitability_reconciles_with_pl(base):
    for block in base["productProfitability"]:
        year = str(block["year"])
        assert sum(p["revenue"] for p in block["products"]) == pytest.approx(
            base["annual"][year]["revenue"], abs=1e-6
        )
        assert sum(p["cogs"] for p in block["products"]) == pytest.approx(
            base["annual"][year]["cogs"], abs=1e-6
        )
    assert base["productProfitability"][-1]["products"][7]["revenue"] / base["annual"]["2028"]["revenue"] == pytest.approx(
        0.143, abs=0.001
    )


def test_expected_payload_is_deterministic(tmp_path, contract):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    write_expected(contract, first)
    write_expected(contract, second)
    assert first.read_bytes() == second.read_bytes()
    payload = json.loads(first.read_text(encoding="utf-8"))
    assert set(payload["scenarios"]) == set(SCENARIO_KEYS)
    for scenario in payload["scenarios"].values():
        assert set(scenario["annual"]) == {"2026", "2027", "2028"}
        assert scenario["cumulativeFcfe"] is not None
    assert payload["contract"]["mixTotal"] == 100
    assert payload["contract"]["seasonalityTotal"] == 12
    assert payload["contract"]["openingDaysTotal"] == 312
    assert payload["contract"]["sources"] == payload["contract"]["uses"] == 160000
    assert payload["meta"]["tolerance"] == {"eur": 1, "pp": 0.1}


def test_committed_expected_matches_engine():
    contract = load_model()
    committed = json.loads(Path(EXPECTED_PATH).read_text(encoding="utf-8"))
    assert expected_payload(contract) == committed


def test_loan_monthly_payment_matches_the_brief():
    assert loan_payment(70000, 0.075, 60) == pytest.approx(1402.66, abs=0.005)
    assert not math.isnan(loan_payment(70000, 0.0, 60))
