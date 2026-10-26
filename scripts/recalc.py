"""Recalcula el libro con el motor `formulas` y compara con los objetivos.

Uso:
    python scripts/recalc.py --json /tmp/recalc.json

No sustituye a Excel: es la puerta automática de CI. Si una función no está
soportada por el motor de validación se documenta y se aísla en los tests.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

WORKBOOK_PATH = ROOT / "docs" / "assets" / "Cafeteria-Aurora-Modelo-Financiero.xlsx"
EXPECTED_PATH = ROOT / "data" / "expected.json"

ERROR_VALUES = ("#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#N/A", "#NUM!", "#NULL!")


def _scalar(value: Any) -> Any:
    if hasattr(value, "value"):
        value = value.value
    try:
        import numpy as np

        array = np.asarray(value)
        if array.size == 0:
            return None
        value = array.ravel()[0]
        if isinstance(value, np.generic):
            value = value.item()
    except Exception:
        pass
    if hasattr(value, "item") and not isinstance(value, (str, bytes)):
        try:
            value = value.item()
        except Exception:
            pass
    return value


def recalculate(path: Path = WORKBOOK_PATH) -> dict[str, dict[str, Any]]:
    import formulas

    model = formulas.ExcelModel().loads(str(path)).finish()
    solution = model.calculate()
    cells: dict[str, dict[str, Any]] = {}
    pattern = re.compile(r"!([A-Z0-9]+)$")
    for key, value in solution.items():
        match = pattern.search(key)
        if not match:
            continue
        sheet_match = re.search(r"\[[^\]]+\]([A-Z0-9]+)'?!", key)
        if not sheet_match:
            continue
        sheet = sheet_match.group(1)
        cells.setdefault(sheet, {})[match.group(1)] = _scalar(value)
    return cells


def errors(cells: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for sheet, values in cells.items():
        for cell, value in values.items():
            if isinstance(value, str) and value in ERROR_VALUES:
                found.append({"sheet": sheet, "cell": cell, "value": value})
    return found


def key_values(cells: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Valores anuales que la auditoría compara con expected.json."""
    out: dict[str, Any] = {}
    for scenario, sheet in (("pessimistic", "PESIMISTA"), ("base", "BASE"), ("optimistic", "OPTIMISTA")):
        values = cells.get(sheet, {})
        out[scenario] = {
            "revenue2026": values.get("B76"),
            "revenue2027": values.get("C76"),
            "ebitda2026": values.get("B86"),
            "ebitda2027": values.get("C86"),
            "netIncome2026": values.get("B92"),
            "netIncome2027": values.get("C92"),
            "closingCash2026": values.get("N48"),
            "closingCash2027": values.get("Z48"),
            "revenue2028": values.get("D76"),
            "ebitda2028": values.get("D86"),
            "netIncome2028": values.get("D92"),
            "closingCash2028": values.get("AL48"),
            "paybackProject": values.get("B113"),
            "paybackEquity": values.get("B114"),
            "cumulativeFcfe": values.get("AL110"),
            "cashOnCash": values.get("B106"),
            "dscr2028": values.get("D105"),
            "breakEvenTotal2026": values.get("B103"),
            "safetyMargin2026": values.get("B104"),
            "checkCash2026": values.get("N50"),
            "checkProduct2028": values.get("C149"),
            "checkTax2028": values.get("D70"),
        }
    out["summary"] = {
        "selector": cells.get("RESUMEN", {}).get("B4") if "RESUMEN" in cells else None,
        "kpiBase2026": cells.get("RESUMEN", {}).get("C10") if "RESUMEN" in cells else None,
    }
    return out


def compare_with_golden(values: dict[str, Any], expected_path: Path = EXPECTED_PATH) -> list[str]:
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    problems: list[str] = []
    mapping = {
        "revenue2026": ("annual", "2026", "revenue"),
        "ebitda2026": ("annual", "2026", "ebitda"),
        "netIncome2026": ("annual", "2026", "netIncome"),
        "closingCash2026": ("annual", "2026", "closingCash"),
        "revenue2027": ("annual", "2027", "revenue"),
        "ebitda2027": ("annual", "2027", "ebitda"),
        "netIncome2027": ("annual", "2027", "netIncome"),
        "closingCash2027": ("annual", "2027", "closingCash"),
        "revenue2028": ("annual", "2028", "revenue"),
        "ebitda2028": ("annual", "2028", "ebitda"),
        "netIncome2028": ("annual", "2028", "netIncome"),
        "closingCash2028": ("annual", "2028", "closingCash"),
        "breakEvenTotal2026": ("annual", "2026", "breakEvenTotal"),
        "safetyMargin2026": ("annual", "2026", "safetyMargin"),
        "dscr2028": ("annual", "2028", "dscr"),
    }
    for scenario, metrics in values.items():
        if scenario == "summary":
            continue
        golden = expected["scenarios"][scenario]
        for metric, (section, year, field) in mapping.items():
            actual = metrics.get(metric)
            wanted = golden[section][year][field]
            if actual is None:
                problems.append(f"{scenario}/{metric}: vacío")
                continue
            try:
                number = float(actual)
            except (TypeError, ValueError):
                problems.append(f"{scenario}/{metric}: no numérico ({actual!r})")
                continue
            tolerance = 1.0 if field not in ("safetyMargin",) else 0.001
            if abs(number - float(wanted)) > tolerance:
                problems.append(
                    f"{scenario}/{metric}: libro {number:.4f} vs golden {float(wanted):.4f}"
                )
        if metrics.get("paybackProject") == ">36":
            book_payback = None
        else:
            book_payback = metrics.get("paybackProject")
        if book_payback != golden["paybackProjectMonths"]:
            problems.append(
                f"{scenario}/payback: libro {book_payback!r} vs golden {golden['paybackProjectMonths']!r}"
            )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Recalcula el libro y audita sus fórmulas")
    parser.add_argument("--xlsx", default=str(WORKBOOK_PATH))
    parser.add_argument("--json", help="Escribe el resultado completo en este JSON")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    cells = recalculate(Path(args.xlsx))
    values = key_values(cells)
    problems = compare_with_golden(values)
    error_list = errors(cells)
    payload = {
        "workbook": str(Path(args.xlsx)),
        "sheets": sorted(cells),
        "keyValues": values,
        "errors": error_list,
        "goldenProblems": problems,
    }
    if args.json:
        Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    if error_list or problems:
        return 1
    print("Recalculación OK: sin errores de fórmula y cifras alineadas con el golden.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
