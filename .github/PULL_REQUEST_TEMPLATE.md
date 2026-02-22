> [!WARNING]
> This repository is archived and no longer actively maintained. It remains public for study purposes only, and there is no guarantee of response, review, or merge.

## Summary
- Describe what changed and why.

## Checklist
- [ ] Lint passes locally
- [ ] Tests pass locally
- [ ] Security impact reviewed
- [ ] Documentation updated
- [ ] Conventional Commit title used

## Validation
- Commands executed:
  - `./.venv/Scripts/python.exe -m ruff check .`
  - `./.venv/Scripts/python.exe -m pytest -q`
  - `./.venv/Scripts/python.exe -m pip_audit -r requirements.txt`
