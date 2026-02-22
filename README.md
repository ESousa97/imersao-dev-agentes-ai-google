# Botinho

> Assistente virtual com FastAPI e Google Gemini para suporte interno de TI e políticas corporativas.

![CI](https://github.com/ESousa97/imersao-dev-agentes-ai-google/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/github/license/ESousa97/imersao-dev-agentes-ai-google)
![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)
![Last Commit](https://img.shields.io/github/last-commit/ESousa97/imersao-dev-agentes-ai-google)
![Issues](https://img.shields.io/github/issues/ESousa97/imersao-dev-agentes-ai-google)

Botinho entrega uma API HTTP e uma interface web para atendimento técnico orientado por contexto de conversa. O projeto roda com fallback de base de conhecimento quando a chave do Gemini não está configurada, mantendo disponibilidade local para desenvolvimento e testes. A arquitetura foi modularizada para facilitar manutenção, segurança e evolução incremental.

## Demonstration

- Interface local: `http://localhost:8000`
- Exemplo de chamada API:

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Como resetar minha senha?","session_id":"demo-1"}'
```

## Technology stack

- Python 3.10+
- FastAPI: API e servidor web
- Uvicorn: ASGI runtime
- Google Gemini (`google-generativeai`): geração de respostas por LLM
- Pydantic + pydantic-settings: contratos de dados e configuração por ambiente
- Ruff + Pytest + pip-audit: qualidade e segurança

## Prerequisites

- Python 3.10 ou superior
- pip
- (Opcional) chave de API Gemini para respostas com IA

## Installation and usage

```bash
python -m venv .venv
.venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
python botinho.py
```

Abra `http://localhost:8000`.

## Available scripts and commands

| Command | Purpose |
| --- | --- |
| `python botinho.py` | Inicia a aplicação local |
| `python diagnostico.py` | Executa diagnóstico do ambiente |
| `./.venv/Scripts/python.exe -m ruff check .` | Lint |
| `./.venv/Scripts/python.exe -m pytest -q` | Testes |
| `./.venv/Scripts/python.exe -m pip_audit -r requirements.txt` | Auditoria de segurança |
| `./scripts/validate.ps1` | Pipeline local de validação |

## Architecture

```text
src/
  botinho/
    main.py              # Rotas FastAPI e middlewares
    settings.py          # Configuração por variáveis de ambiente
    security.py          # Rate limit e security headers
    services/
      chat_service.py    # Lógica de negócio e memória de conversa
    static/              # Frontend estático
tests/
  unit/
  integration/
```

Detalhes adicionais em:
- `docs/architecture.md`
- `docs/api.md`
- `docs/setup.md`
- `docs/deployment.md`

## API reference

- `GET /`
- `GET /health`
- `POST /api/chat`
- `GET /api/conversation/{session_id}`
- `GET /api/stats`

Consulte `docs/api.md` para payloads e respostas.

## Roadmap

- [x] Modularização do backend
- [x] Contratos de API com validação
- [x] Rate limiting e security headers
- [x] CI com lint, testes e audit
- [ ] Persistência de conversas em banco de dados
- [ ] Migração para SDK Gemini mais recente (`google-genai`)

## Contributing

Veja `CONTRIBUTING.md`.

## License

Projeto licenciado sob MIT. Consulte `LICENSE`.

## Author

- Enoque Sousa
- Portfólio: https://enoquesousa.vercel.app
- GitHub: https://github.com/ESousa97
