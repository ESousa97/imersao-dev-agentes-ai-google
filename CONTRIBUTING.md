# Contributing

## Repository archive status

This repository is no longer active and is archived.
It remains public only for study and reference purposes.
There is no guarantee of response, review, or correction for issues and pull requests.

## Development setup
1. Create virtual environment and activate it.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and provide `GEMINI_API_KEY`.
4. Run locally with `python botinho.py`.

## Code style
- Linting and formatting use Ruff configuration from `pyproject.toml`.
- Keep functions small and cohesive.
- Keep API errors in the standard format `{ "error": { "code", "message", "details?" } }`.

## Branch and commit conventions
- Branch naming: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `chore/<topic>`.
- Commit style (Conventional Commits):
  - `feat:` new feature
  - `fix:` bug fix
  - `refactor:` internal refactor without behavior change
  - `docs:` documentation
  - `style:` formatting only
  - `test:` tests
  - `chore:` maintenance/config/dependencies
  - `ci:` CI/CD changes
  - `perf:` performance improvement
  - `security:` security fixes

## Pull request process
1. Open a PR against `main`.
2. Fill in the PR template checklist.
3. Ensure CI passes (lint, test, security audit).
4. Request at least one review before merge.

## Running quality checks
- `./.venv/Scripts/python.exe -m ruff check .`
- `./.venv/Scripts/python.exe -m pytest -q`
- `./.venv/Scripts/python.exe -m pip_audit -r requirements.txt`

## Where contributions are welcome
- Knowledge base enrichment.
- UX improvements in the static chat client.
- Additional integration tests for API endpoints.

## Author
- Portfolio: https://enoquesousa.vercel.app
- GitHub: https://github.com/ESousa97
