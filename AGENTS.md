# AGENTS.md

## Agent skills

### Issue tracker

Issues and specs live as GitHub issues in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles use the default label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Repository expectations

- Read `GLOSSARY.md` before naming financial concepts.
- Read `docs/adr/` before changing the model architecture.
- The assumptions contract and golden outputs live in `docs/project-brief.md`; `data/model.json` is the executable source of truth and must match it.
- Financial formulas are the product: never hardcode a calculated value where a live formula belongs.
- The Excel workbook is generated from the shared input file; do not hand-edit generated workbooks.
- Run the checks in `README.md` before opening a pull request.
