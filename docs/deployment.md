# Deployment

## Runtime model
Single process FastAPI app serving API and static files.

## Production recommendations
1. Set `BOTINHO_ENV=production`.
2. Set explicit `BOTINHO_CORS_ALLOWED_ORIGINS` with trusted domains only.
3. Configure `GEMINI_API_KEY` from secret manager.
4. Run behind reverse proxy (Nginx/Traefik) with TLS termination.

## Example with Uvicorn
```bash
python -m uvicorn src.botinho.main:app --host 0.0.0.0 --port 8000
```

## Health checks
Use `GET /health` for liveness and readiness probes.

## Security baseline in app
- Structured API errors.
- Basic per-IP rate limiting.
- Security headers middleware.
- Restricted CORS configuration by environment variable.
