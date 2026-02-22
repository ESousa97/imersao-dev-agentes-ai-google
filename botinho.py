"""Backward-compatible executable entrypoint for Botinho."""

from __future__ import annotations

import sys
from pathlib import Path

import uvicorn

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from botinho.settings import get_settings  # noqa: E402

settings = get_settings()


if __name__ == "__main__":
    browser_host = settings.host
    print(f"Servidor iniciando em bind {settings.host}:{settings.port}")
    print(f"Abra no navegador: http://{browser_host}:{settings.port}")

    uvicorn.run(
        "botinho.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
    )