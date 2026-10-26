"""Comprueba enlaces y recursos relativos del sitio construido en docs/."""

from __future__ import annotations

import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value for key, value in attrs if value is not None}
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag in {"a", "link", "img", "script", "source"}:
            target = attributes.get("href") or attributes.get("src")
            if target:
                self.links.append((tag, target))


def _html_files() -> list[Path]:
    return sorted(DOCS.glob("*.html"))


def check(docs: Path = DOCS) -> list[str]:
    problems: list[str] = []
    parsed: dict[Path, LinkParser] = {}
    for page in sorted(docs.glob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed[page] = parser

    for page, parser in parsed.items():
        for tag, raw in parser.links:
            target = raw.strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
                continue
            path_part, _, anchor = target.partition("#")
            if path_part in ("", "."):
                target_page = page
            else:
                target_page = (page.parent / path_part).resolve()
            try:
                target_page.relative_to(docs.resolve())
            except ValueError:
                problems.append(f"{page.name}: enlace fuera de docs/ ({tag} {raw})")
                continue
            if not target_page.exists():
                problems.append(f"{page.name}: no existe {raw}")
                continue
            if anchor and target_page.suffix == ".html":
                target_parser = parsed.get(target_page)
                if target_parser is None:
                    target_parser = LinkParser()
                    target_parser.feed(target_page.read_text(encoding="utf-8"))
                    parsed[target_page] = target_parser
                if anchor not in target_parser.ids:
                    problems.append(f"{page.name}: ancla inexistente {raw}")
            if tag == "img" and not target_page.is_file():
                problems.append(f"{page.name}: imagen inexistente {raw}")

    # Los enlaces del README que apuntan a artefactos locales también deben existir.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", readme):
        link = html.unescape(match.group(1)).split("#")[0]
        if not link or link.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        if not (ROOT / link).exists():
            problems.append(f"README.md: no existe {link}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Comprueba enlaces relativos de docs/ y README")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    problems = check()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        return 1
    if not args.quiet:
        print("Enlaces relativos: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
