# Setup Guide

## Prerequisites
- Python 3.10+
- pip

## Installation
```bash
python -m venv .venv
.venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Environment
```bash
copy .env.example .env
```

Set `GEMINI_API_KEY` in `.env` to enable AI-generated responses.
Without API key, Botinho runs in knowledge-base fallback mode.

## Run locally
```bash
python botinho.py
```

## Quality checks
```bash
./.venv/Scripts/python.exe -m ruff check .
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe -m pip_audit -r requirements.txt
```
