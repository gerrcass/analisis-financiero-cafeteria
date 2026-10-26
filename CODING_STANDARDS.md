# CODING_STANDARDS.md

These are the rules the reviewer enforces. They are written as judgment calls plus the mechanical checks that make each one observable.

## 1. The model contract is sacred

- `data/model.json` is the only source of inputs. If a value is needed in two places, derive it or reference it; never duplicate the literal.
- `docs/project-brief.md` is the frozen assumptions and formula contract. A code change that changes an economic definition must update the brief, the golden outputs, the workbook, the site and the tests in the same pull request.
- A calculated value is never committed as an input. The only constants allowed are labels, dates that define the calendar, scenario selectors, and the input values explicitly listed in the brief.
- Tolerances are fixed: ±1 € for amounts, ±0.1 pp for margins, exact month for payback. Do not widen them to make a test pass.

## 2. Live formulas in the workbook

- Every calculated cell in a scenario sheet and in the summary is a formula. This is audited mechanically: the test counts formulas and inspects the key rows.
- Input cells are visually marked and confined to `Supuestos`, `Productos`, `Personal`, `Costos` and cover metadata.
- Formulas must be copied consistently across the three scenario sheets. The test normalizes the formulas and compares the three structures.
- Use plain Excel functions that survive recalculation: `IF`, `IFERROR`, `INDEX`, `MATCH`, `SUM`, `SUMIF`, `SUMPRODUCT` over ranges, `PMT`, `CHOOSE`, `MAX`, `MIN`, `ROUND`, `ROUNDUP`, `EDATE`, `DATE`, `MOD`, `ABS`.
- Avoid dynamic-array functions, `XLOOKUP`, `IFS`, external workbook links, volatile functions and array constants inside `SUMPRODUCT`; the validation engine and older Excel clients may not handle them.
- Set full recalculation on load. If cached values are written, they must be the result of a real recalculation, not invented numbers.
- Every workbook must include visible integrity checks and a test that confirms no `#REF!`, `#VALUE!`, `#DIV/0!` or empty key cells remain.
- Charts must reference cell ranges, never static images. A chart with a hardcoded series is a bug.

## 3. Python engine

- Pure functions with type hints. No mutation of the input contract.
- Use `Decimal` only where it prevents a real rounding defect; otherwise floats with the documented tolerance.
- The engine returns a typed structure with annual and monthly projections, plus checks. It does not format output for a specific UI.
- The CLI writes deterministic JSON: stable key order, two-decimal rounding for amounts, percentages as decimals.
- Tests cover each block and the identities in `docs/project-brief.md#6-modelo-matemático`.
- A test that only asserts "does not crash" is not a test. Assert a number, an identity or an ordering.

## 4. JavaScript engine and site

- ES modules, no runtime dependencies, no CDN, no external fonts. The site must work offline after build.
- The browser engine mirrors the Python engine's public shape and uses the same domain names. A JS/Python divergence is a failing test.
- DOM rendering must be accessible: semantic landmarks, labelled controls, visible focus, `aria-pressed` for toggles, `<table>` with `<caption>`/`<th>`, and SVG charts with `<title>` and `<desc>`.
- Never inject untrusted strings with `innerHTML`. The model contract is local, but keep the habit.
- Charts must be readable at 390 px and 1440 px; use a responsive `viewBox` and a text alternative.
- URL state is a feature: scenario, year and lab overrides must survive a reload and be shareable. Invalid values must fall back to the documented defaults.
- The lab is a sandbox. It must not mutate the source contract; reset must restore the selected scenario exactly.
- Prefer small pure functions (`calculateProjection`, `formatCurrency`, `chartSeries`) over DOM-coupled logic. Test the pure part.

## 5. Content and copy

- Spanish, tuteo, warm and precise. Explain a term the first time it appears.
- Every number in the guide must come from the model or from a cited benchmark. Do not invent a source.
- The guide teaches the *why* before the formula, then applies the formula to Aurora, then names the common mistake. Exercises must have answers.
- The site and the workbook must show the Pesimista case with the same prominence as the Base.
- Include the disclaimer: educational model, not financial, tax or legal advice.
- Avoid promises of returns and avoid "garantizado", "sin riesgo" or similar.

## 6. Visual system

- Follow `docs/design-brief.md`: cream paper, espresso, terracotta, sage; editorial serif for display, sans for UI; calm motion.
- Use design tokens for color, spacing, radius and type. No one-off hex values in components.
- No stock-photo clichés, no coffee-bean wallpaper, no gradients that fight the content.
- Data density is allowed; clutter is not. Every chart has a title, a unit and a one-line reading.
- Mobile is not a shrunken desktop: tables get a deliberate overflow or stacked treatment, controls stay reachable, and the first viewport still answers "what is this?".

## 7. Tests and evidence

- Test external behaviour. A good test fails when a user-visible number, formula, or interaction changes.
- Prefer the highest seam: contract → engine outputs; workbook → recalculated values; built site → DOM. Do not test private helpers just because they are easy.
- Every bug fix gets a regression test that fails on the old behaviour.
- Workbook tests must inspect formulas, not only cached values.
- Browser tests must check a real interaction and the resulting DOM, not just that the page loaded.
- CI runs the same commands a contributor runs locally. If a check is too slow for every push, it still runs on every pull request.
- A pull request includes evidence attached with `gh --attach`: before/after screenshot for visual work, command output for logic work, formula-audit summary for workbook work.
- Test output must be deterministic; do not depend on the current date, network or a user's locale. Money is EUR, percentages use a dot in code.

## 8. Pull requests and review

- Use the `pr` skill template: summary, evidence, merge danger, blast radius.
- Keep pull requests scoped to one ticket. A refactor that is not needed for the ticket belongs in its own pull request.
- The reviewer checks: formulas live, inputs confined, Python/JS parity, golden outputs unchanged or intentionally updated everywhere, guide numbers match, accessibility basics, no console errors, no broken relative links.
- A "two-way door" change can merge with a green check and evidence. A change that alters the assumptions contract is a one-way door: it needs the brief, golden outputs and all artifacts updated together.
- Do not merge with a failing check, an unresolved review comment, or an artifact that only exists on the contributor's machine.
