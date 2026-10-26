"""Contraste del motor con los objetivos dorados congelados.

Cita: docs/project-brief.md §7.5 y §6.13. Tolerancia ±1 € y ±0,1 pp.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.model import MARGIN_FIELDS, SCENARIO_KEYS, build_model, load_model

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = json.loads((ROOT / "data" / "expected.json").read_text(encoding="utf-8"))
TOLERANCE_EUR = EXPECTED["meta"]["tolerance"]["eur"]
TOLERANCE_PP = EXPECTED["meta"]["tolerance"]["pp"] / 100


@pytest.fixture(scope="module")
def contract():
    return load_model()


def test_expected_has_three_scenarios_and_three_years():
    assert set(EXPECTED["scenarios"]) == set(SCENARIO_KEYS)
    for scenario in EXPECTED["scenarios"].values():
        assert set(scenario["annual"]) == {"2026", "2027", "2028"}


@pytest.mark.parametrize("scenario_key", SCENARIO_KEYS)
def test_engine_matches_golden_annual(contract, scenario_key):
    result = build_model(contract, scenario_key)
    golden = EXPECTED["scenarios"][scenario_key]
    for year, fields in golden["annual"].items():
        for field, wanted in fields.items():
            tolerance = TOLERANCE_PP if field in MARGIN_FIELDS else TOLERANCE_EUR
            actual = result["annual"][year][field]
            assert actual == pytest.approx(wanted, abs=tolerance), (
                f"{scenario_key}/{year}/{field}: {actual} != {wanted} "
                f"(tolerancia {tolerance})"
            )


@pytest.mark.parametrize("scenario_key", SCENARIO_KEYS)
def test_engine_matches_golden_payback_and_return(contract, scenario_key):
    result = build_model(contract, scenario_key)
    golden = EXPECTED["scenarios"][scenario_key]
    assert result["paybackProjectMonths"] == golden["paybackProjectMonths"]
    assert result["paybackEquityMonths"] == golden["paybackEquityMonths"]
    assert result["cumulativeFcfe"] == pytest.approx(golden["cumulativeFcfe"], abs=TOLERANCE_EUR)
    assert result["cashOnCash"] * 100 == pytest.approx(golden["cashOnCash"], abs=0.1)


def test_product_block_matches_golden(contract):
    for scenario_key in SCENARIO_KEYS:
        result = build_model(contract, scenario_key)
        golden = EXPECTED["scenarios"][scenario_key]["productProfitability"]
        for block, golden_block in zip(result["productProfitability"], golden):
            assert block["year"] == golden_block["year"]
            for product, golden_product in zip(block["products"], golden_block["products"]):
                assert product["name"] == golden_product["name"]
                assert product["revenue"] == pytest.approx(golden_product["revenue"], abs=TOLERANCE_EUR)
                assert product["cogs"] == pytest.approx(golden_product["cogs"], abs=TOLERANCE_EUR)
                assert product["marginPct"] * 100 == pytest.approx(
                    golden_product["marginPct"], abs=0.1
                )


def test_reproducible_build_is_clean():
    """`make model` no debe dejar deriva: el test compara contenido, no mtime."""
    contract = load_model()
    before = (ROOT / "data" / "expected.json").read_text(encoding="utf-8")
    from scripts.model import write_expected

    write_expected(contract)
    after = (ROOT / "data" / "expected.json").read_text(encoding="utf-8")
    assert before == after
