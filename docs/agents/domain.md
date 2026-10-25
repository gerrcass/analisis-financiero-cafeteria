# Domain Docs

How the engineering skills should consume this repo's domain documentation.

## Before exploring, read these

- **`GLOSSARY.md`** at the repo root.
- **`docs/adr/`**: read ADRs that touch the area you are about to work in.

If any of these files do not exist, proceed silently. The `/domain-modeling` skill creates them lazily when terms or decisions are actually resolved.

## File structure

Single-context repo:

```
/
├── GLOSSARY.md
├── docs/adr/
└── src/
```

## Use the glossary's vocabulary

When naming a domain concept in code, tests, issues or docs, use the term as defined in `GLOSSARY.md`. Do not drift to synonyms the glossary explicitly avoids.

## Flag ADR conflicts

If an output contradicts an existing ADR, surface it explicitly rather than silently overriding it.
