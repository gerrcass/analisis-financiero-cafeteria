# AGENTS.md

## Start here

- **Assumptions, formulas and golden outputs**: `docs/project-brief.md`. Treat it as the frozen contract. If a change contradicts it, surface the contradiction instead of silently diverging.
- **Domain vocabulary**: `GLOSSARY.md`. Use its terms in code, tests, issues and copy.
- **Architecture decisions**: `docs/adr/`. Read the relevant ADR before changing the model, the workbook generator or the site architecture.
- **Current work**: `docs/specs/001-modelo-financiero-cafeteria.md` and the GitHub issues it links.
- **Review rules**: `CODING_STANDARDS.md`. These are enforced by review, not by implementation.

## Working agreements

- One source of truth: `data/model.json`. The Python engine, the JavaScript engine, the workbook and the site all derive from it.
- Financial formulas are the product. Calculated cells in the workbook and calculated values in the site must be live and derived from inputs.
- Inputs live only in the assumption sheets. Scenario and summary sheets are formulas.
- Keep Python and JavaScript engines behaviourally identical. A difference is a failing test, not an editorial choice.
- The Pesimista scenario is the stress test. Do not hide or flatter it.
- The guide is teaching material, not marketing copy. Use the model's real numbers, explain the jargon and state the assumptions.
- All work in this repo uses DeepSeek V4.1 Flash (variant Max). Do not delegate to another model.

## Commands

The canonical commands will be provided by the implementation. They are the contract:

```bash
make setup      # install Python venv + Node test dependencies
make model      # regenerate data/expected.json from data/model.json
make workbook   # regenerate the .xlsx
make site       # regenerate the static site in docs/
make test       # Python + Node + workbook + browser tests
make check      # build + test + verify docs/ artifacts are current
make serve      # serve docs/ locally for browser checks
```

If a command does not exist yet, create it as part of the ticket that needs it; do not bypass it with a one-off shell command.

## Verification

- Run `make check` before opening or updating a pull request.
- Attach evidence to every pull request with `gh --attach`: a screenshot for visual work, command output for logic work, and the formula-audit result for workbook work.
- A pull request is not ready until the spec and ticket acceptance criteria are satisfied and the evidence is attached.
- Leave `main` reproducible: generated artifacts committed, tests green, no open issues or pull requests without a stated reason.

## Agent skills

### Issue tracker

Issues and specs live as GitHub issues in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles use the default label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
