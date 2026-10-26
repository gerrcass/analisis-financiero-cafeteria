"""Genera la captura del dashboard real con Playwright.

Requiere `npm install` y el sitio construido en `docs/`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    result = subprocess.run(["node", "scripts/screenshot.mjs"], cwd=ROOT, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
