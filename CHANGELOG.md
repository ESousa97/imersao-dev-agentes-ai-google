# Changelog

All notable changes to this project are documented in this file.

The format follows Keep a Changelog and this project follows Semantic Versioning.

## [2.1.1] - 2026-02-21

### Changed
- Marked the repository as archived/study-only in governance documents.
- Added visible archive warnings to issue and pull request templates.
- Kept blank issue creation disabled and added archived-project notice link in issue config.
- Disabled Dependabot pull request creation for all configured ecosystems.

## [2.1.0] - 2026-02-21

### Added
- New modular backend architecture under `src/botinho`.
- Environment-based settings with `.env.example`.
- Structured API error envelope.
- Security headers middleware and in-memory rate limiting.
- Static frontend split into HTML/CSS/JS with centralized style tokens.
- Unit and integration tests.
- Ruff, pytest and pip-audit toolchain.
- GitHub governance files: CI workflow, Dependabot, issue templates, PR template, CODEOWNERS.
- New complementary docs: architecture, api, setup and deployment.

### Changed
- `botinho.py` converted to backward-compatible runner.
- Input contract now validates payload and accepts legacy field `mensagem`.
- Project README rewritten to reflect production-grade setup.
- Diagnostics script updated for env-based configuration.

### Removed
- Hardcoded API key configuration pattern.
- Monolithic inline frontend and duplicated style blocks.

### Fixed
- Inconsistent API payload naming across docs and implementation.
- Missing validation and unsafe error response patterns.
- Missing repository-level engineering standards and contribution workflow.

### Security
- Added baseline HTTP security headers.
- Added dependency audit in local/CI validation.
- Added explicit guidance for responsible vulnerability disclosure.

## [1.0.0] - 2025-09-22

### Added
- Initial release with FastAPI chat and Gemini integration.
