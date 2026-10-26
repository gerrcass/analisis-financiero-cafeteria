"""El verificador de artefactos debe ignorar el ZIP y comparar semántica."""

from __future__ import annotations

from pathlib import Path

from scripts.build_workbook import build_workbook
from scripts.verify_artifacts import verify, workbook_signature


def test_workbook_semantics_do_not_depend_on_zip_timestamps(tmp_path):
    first = tmp_path / "first.xlsx"
    second = tmp_path / "second.xlsx"
    build_workbook(output=first)
    build_workbook(output=second)
    assert workbook_signature(first) == workbook_signature(second)
    assert first.exists() and second.exists()


def test_committed_artifacts_are_semantically_current():
    assert verify() == []
    assert Path("docs/assets/screenshot-dashboard.png").exists()
