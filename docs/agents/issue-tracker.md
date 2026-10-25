# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues in `gerrcass/analisis-financiero-cafeteria`. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body-file <file>`.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments`.
- **Blocking**: use GitHub's native issue dependencies with `gh issue create --blocked-by <n>` or `gh api --method POST repos/{owner}/{repo}/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`.
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`.
- **Close**: `gh issue close <number> --comment "..."`.

## Pull requests as a triage surface

**PRs as a request surface: no.**

When a skill says "publish to the issue tracker", create a GitHub issue. When it says "fetch the relevant ticket", read it as above. GitHub shares one number space across issues and PRs, so resolve a bare `#42` with `gh pr view 42` and fall back to `gh issue view 42`.

## Wayfinding operations

- **Blocking**: native issue dependencies (see above). Fall back to a `Blocked by: #<n>` line only if the API rejects the edge.
- **Frontier query**: open issues with no open blocker and no assignee.
- **Claim**: `gh issue edit <n> --add-assignee @me`.
- **Resolve**: comment with evidence, close, and update the parent spec.
