$ErrorActionPreference = "Stop"

$python = "./.venv/Scripts/python.exe"

& $python -m ruff check .
& $python -m pytest -q
& $python -m pip_audit -r requirements.txt
