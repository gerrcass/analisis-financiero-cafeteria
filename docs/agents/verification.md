# Verification

The canonical gates for every pull request. `AGENTS.md` points here; the commands live in the repository so this file does not restate them.

## Fast loop

Use while implementing:

```bash
make test        # or the narrower test target for the module you touched
```

## Full loop

Before opening or updating a pull request:

```bash
make check       # build + all tests + docs freshness
```

`make check` must be green from a clean checkout. If it is not runnable from a clean checkout, fix the setup before adding features.

## Evidence matrix

| Work | Evidence attached to the PR |
|---|---|
| Model engine | `make model` output, Python/Node test summary, golden-output diff |
| Workbook structure | formula-audit summary, recalculation result, screenshot of the opened book if available |
| Workbook summary/charts | screenshot of the five charts, chart-series audit, recalculation result |
| Site dashboard | 1440×900 screenshot, mobile 390 px screenshot, browser test output |
| Lab and guide | screenshot of a changed assumption and its delta, guide chapter count, content test |
| Deployment | public URL, README screenshot, CI run URL, Lighthouse or equivalent summary |

Use `gh --attach` on the pull request or on a follow-up comment:

```bash
gh pr comment <number> --attach ./before.png --attach ./after.png --body "Evidence"
```

Screenshots belong in the PR, not only in the repository. The README screenshot is a separate deliverable: it must be committed and show the real deployed dashboard.

## Environment notes

- Python 3.10+, Node.js 22+, `make`, `gh` authenticated.
- No `sudo` and no LibreOffice in this environment. Use the Python `formulas` package as the recalculation check and keep formulas inside its supported subset. An optional LibreOffice path can be added for contributors who have it.
- Playwright browsers are available in the user cache; use `npx playwright test` with the installed version.
- GitHub Pages serves `docs/` from `main`.
- Do not commit `.venv/`, `node_modules/`, `.scratch/` or browser artifacts.
