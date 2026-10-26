"""Contenido de la guía: capítulos, ejercicios, respuestas y cifras del modelo."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "docs" / "guia-finanzas.md"
GUIDE_HTML = ROOT / "docs" / "aprende.html"
EXPECTED = json.loads((ROOT / "data" / "expected.json").read_text(encoding="utf-8"))


def _chapter_blocks() -> list[str]:
    text = GUIDE.read_text(encoding="utf-8")
    parts = re.split(r"^## Capítulo \d+ — .*$", text, flags=re.M)
    return parts[1:]


def test_guide_has_ten_named_chapters():
    text = GUIDE.read_text(encoding="utf-8")
    titles = re.findall(r"^## Capítulo (\d+) — (.+?) \{#capitulo-\1\}$", text, flags=re.M)
    assert len(titles) == 10
    assert [int(number) for number, _ in titles] == list(range(1, 11))
    assert "Qué es un modelo financiero" in titles[0][1]
    assert "Decidir con el modelo" in titles[9][1]


def test_guide_has_36_exercises_and_36_answers():
    exercise_total = 0
    answer_total = 0
    for block in _chapter_blocks():
        if "### Ejercicios" not in block or "### Respuestas" not in block:
            continue
        exercises = block.split("### Ejercicios", 1)[1].split("### Respuestas", 1)[0]
        answers = block.split("### Respuestas", 1)[1].split("\n## ", 1)[0]
        exercise_total += len(re.findall(r"^\d+\. ", exercises, flags=re.M))
        answer_total += len(re.findall(r"^\d+\. ", answers, flags=re.M))
    assert exercise_total == 36
    assert answer_total == 36


def test_guide_contains_glossary_checklist_and_workshop():
    text = GUIDE.read_text(encoding="utf-8")
    assert "## Glosario mínimo {#glosario}" in text
    assert "## Checklist de validación {#checklist}" in text
    assert "## Notas para un taller de 90 minutos {#taller}" in text
    glossary = text.split("## Glosario mínimo", 1)[1].split("## Checklist de validación", 1)[0]
    assert len(re.findall(r"^\| [^|]+ \|", glossary, flags=re.M)) >= 13  # 12 términos + cabecera
    checklist = text.split("## Checklist de validación", 1)[1].split("## Notas para un taller", 1)[0]
    assert checklist.count("- [ ]") == 20
    workshop = text.split("## Notas para un taller de 90 minutos", 1)[1]
    assert "Minutos 0–10" in workshop and "Minutos 85–90" in workshop


@pytest.mark.parametrize(
    "figure",
    ["384.419", "61.658", "30.142", "57.456", "132.063", "108.082", "34 meses", "30 meses", ">36"],
)
def test_guide_uses_real_aurora_figures(figure):
    assert figure in GUIDE.read_text(encoding="utf-8")


def test_guide_figures_match_the_golden_model():
    base = EXPECTED["scenarios"]["base"]["annual"]
    assert base["2026"]["revenue"] == pytest.approx(384418.75, abs=1)
    text = GUIDE.read_text(encoding="utf-8")
    assert "384.419" in text
    assert "57.456" in text
    assert "132.063" in text
    assert EXPECTED["scenarios"]["pessimistic"]["annual"]["2028"]["netIncome"] == pytest.approx(133.60, abs=1)
    assert "134 €" in text


def test_published_guide_is_generated_from_markdown():
    html = GUIDE_HTML.read_text(encoding="utf-8")
    assert "{{TOC}}" not in html and "{{CONTENT}}" not in html
    for number in range(1, 11):
        assert f'id="capitulo-{number}"' in html
    assert "Guía de finanzas" in html
    assert "Calculadoras" in html
    assert html.count('class="calc-card"') == 3
    assert "384.419" in html
    assert "108.082" in html
    assert "Glosario mínimo" in html
    assert "Checklist de validación" in html


def test_published_guide_has_exercise_headings():
    html = GUIDE_HTML.read_text(encoding="utf-8")
    assert len(re.findall(r'<h3[^>]*>Ejercicios</h3>', html)) == 10
    assert len(re.findall(r'<h3[^>]*>Respuestas</h3>', html)) == 10
