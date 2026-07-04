# Contributing to Recipe Remix

Thanks for considering a contribution! Here's how to get set up and land a good PR.

## Setup

See the [README](README.md) for full local setup instructions (Docker Postgres + FastAPI backend + Vite frontend).

## Finding something to work on

- Look for issues labeled [`good first issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) — these are scoped to be doable in one sitting.
- Have your own idea? Open an issue describing it before starting work, so we can align before you spend time on it.

Some categories of contribution that don't require deep context on the codebase:

- **Add a substitution**: extend `SUBSTITUTIONS` in `backend/app/seed_data.py` (or submit via the API) with a new ingredient swap and which diets it satisfies.
- **Expand the diet denylist**: add more ingredients to `DIET_DENYLIST` in `backend/app/substitutions.py` so more things get flagged correctly.
- **New dietary filter**: add a new diet tag (e.g. `low_fodmap`, `kosher`) end-to-end — denylist entries, sample substitutions, and a button in `RecipeDetail.jsx`.
- **Frontend polish**: loading states, empty states, accessibility fixes, responsive tweaks.
- **Tests**: both frontend and backend could always use more coverage.

## Pull request checklist

- [ ] Branch from `main`
- [ ] Backend changes: add/update a test in `backend/tests/` and confirm `pytest` passes
- [ ] Frontend changes: confirm `npm run build` succeeds with no errors
- [ ] Keep PRs focused — one logical change per PR is easier to review and merge quickly
- [ ] Describe _why_, not just _what_, in your PR description

## Code style

- **Backend**: standard PEP 8, type hints where practical. Comments should explain _why_ over _what_.
- **Frontend**: functional components, Tailwind utility classes (no separate CSS files per component).

## Reporting bugs / suggesting features

Open an issue using the relevant template. Include repro steps for bugs.

## Commit message convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for commit messages. Format:

    <type>: <short summary>

    <optional longer description>

Common types used in this repo:

| Type       | Use for                                                |
| ---------- | ------------------------------------------------------ |
| `feat`     | A new feature                                          |
| `fix`      | A bug fix                                              |
| `docs`     | Documentation only (README, CONTRIBUTING, comments)    |
| `test`     | Adding or fixing tests, no production code change      |
| `refactor` | Code change that's neither a fix nor a new feature     |
| `chore`    | Maintenance (deps, config, tooling) — no source change |

Examples from this repo:

- `feat: add kosher diet filter`
- `fix: correct gluten-free denylist missing soy sauce`
- `docs: add stop/restart instructions to README`

Not required for every tiny commit, but appreciated on PRs — it makes the history easy to scan and helps us write better release notes later. See the [Conventional Commits spec](https://www.conventionalcommits.org/) for the full set of types and rules (including `!` for breaking changes, scopes, etc.).

## Code of conduct

Be respectful, assume good faith, and keep feedback constructive. This is a learning-friendly project — questions are always welcome.
