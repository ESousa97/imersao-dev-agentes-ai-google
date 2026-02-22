"""FastAPI application entry point."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .models import ChatRequest, ErrorEnvelope
from .security import RateLimitMiddleware, SecurityHeadersMiddleware
from .services.chat_service import ChatService, GeminiClient
from .settings import get_settings

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("botinho")

model_client = GeminiClient(api_key=settings.gemini_api_key, model_name=settings.gemini_model)
chat_service = ChatService(model_client=model_client, logger=logger)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Assistente virtual com FastAPI e Google Gemini.",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    requests_limit=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    envelope = ErrorEnvelope(
        error={
            "code": "validation_error",
            "message": "Payload inválido",
            "details": {"errors": exc.errors()},
        }
    )
    return JSONResponse(status_code=422, content=envelope.model_dump())


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    envelope = ErrorEnvelope(error={"code": "http_error", "message": str(exc.detail)})
    return JSONResponse(status_code=exc.status_code, content=envelope.model_dump())


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Erro não tratado", exc_info=exc)
    envelope = ErrorEnvelope(
        error={"code": "internal_error", "message": "Erro interno inesperado."}
    )
    return JSONResponse(status_code=500, content=envelope.model_dump())


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": settings.app_version, "environment": settings.environment}


@app.post("/api/chat")
async def chat_endpoint(payload: dict):
    request = ChatRequest.model_validate(payload)

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia")

    result = await chat_service.converse(request.message, request.session_id)
    return JSONResponse(jsonable_encoder(result))


@app.get("/api/conversation/{session_id}")
async def conversation_history(session_id: str):
    conversation = chat_service.conversations.get(session_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")

    return JSONResponse(
        {
            "session_id": session_id,
            "created_at": conversation.criado_em.isoformat(),
            "last_category": conversation.ultima_categoria,
            "history_count": len(conversation.historico),
            "history": [entry.model_dump(mode="json") for entry in conversation.historico],
        }
    )


@app.get("/api/stats")
async def stats():
    total_conversations = len(chat_service.conversations)
    total_messages = sum(len(conv.historico) for conv in chat_service.conversations.values())

    return JSONResponse(
        {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "active_sessions": list(chat_service.conversations.keys()),
        }
    )
