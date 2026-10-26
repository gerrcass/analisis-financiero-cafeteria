"""Construye el sitio estático en ``docs/`` desde ``site/``.

No borra la documentación Markdown de ``docs/`` ni los assets generados por el
libro. Copia únicamente la fuente del sitio y genera los artefactos derivados.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.model import load_model  # noqa: E402

SITE = ROOT / "site"
DOCS = ROOT / "docs"
MODEL = ROOT / "data" / "model.json"
BASE_URL = "https://gerrcass.github.io/analisis-financiero-cafeteria/"


def build_site(source: Path = SITE, output: Path = DOCS, model: Path = MODEL) -> Path:
    data = load_model(model)
    output.mkdir(parents=True, exist_ok=True)
    (source / "data").mkdir(parents=True, exist_ok=True)
    shutil.copy2(model, source / "data" / "model.json")

    # Copia la fuente del sitio sin borrar Markdown, ADRs ni assets del libro.
    shutil.copytree(source, output, dirs_exist_ok=True)

    # La marca canónica vive en assets/ y se publica con el sitio.
    mark = ROOT / "assets" / "aurora-mark.svg"
    if mark.exists():
        shutil.copy2(mark, source / "assets" / "aurora-mark.svg")
        shutil.copy2(mark, output / "assets" / "aurora-mark.svg")

    (output / ".nojekyll").write_text("", encoding="utf-8")
    (output / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + BASE_URL + "sitemap.xml\n",
        encoding="utf-8",
    )
    (output / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{BASE_URL}</loc></url>\n"
        f"  <url><loc>{BASE_URL}aprende.html</loc></url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Construye el sitio de Cafetería Aurora")
    parser.add_argument("--source", default=str(SITE))
    parser.add_argument("--output", default=str(DOCS))
    parser.add_argument("--model", default=str(MODEL))
    args = parser.parse_args(argv)
    path = build_site(Path(args.source), Path(args.output), Path(args.model))
    print(f"Sitio construido en {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
