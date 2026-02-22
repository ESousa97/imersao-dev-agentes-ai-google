# Architecture

## Overview
Botinho is a FastAPI application with a lightweight static web client and in-memory conversation context.

## Layers
- API layer: request parsing, validation, HTTP response contracts.
- Service layer: business logic, topic detection, memory handling, model interaction.
- Infra layer: environment settings, security middlewares, static file serving.

## Directory map
- `src/botinho/main.py`: app factory and routes.
- `src/botinho/services/chat_service.py`: conversation business logic.
- `src/botinho/security.py`: rate limit and security headers middleware.
- `src/botinho/settings.py`: environment-based configuration.
- `src/botinho/static/`: web UI assets.

## Architecture decisions
1. Keep in-memory session storage for simplicity and low overhead in MVP scope.
2. Keep Gemini integration abstracted behind `GeminiClient` to support future migration.
3. Serve static assets from FastAPI for single-process deployment.
