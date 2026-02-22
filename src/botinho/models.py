"""Pydantic models used by API contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=100)

    @model_validator(mode="before")
    @classmethod
    def _support_legacy_payload(cls, data: Any) -> Any:
        if isinstance(data, dict) and "message" not in data and "mensagem" in data:
            data = {**data, "message": data["mensagem"]}
        return data


class ChatResponse(BaseModel):
    response: str
    confidence: float
    context_found: bool
    continues_topic: bool
    session_id: str
    timestamp: datetime
    bot_name: str = "Botinho"
    model: str


class ApiError(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ErrorEnvelope(BaseModel):
    error: ApiError


class ConversationMessage(BaseModel):
    usuario: str
    bot: str
    categoria: str | None = None
    timestamp: datetime


class ConversationData(BaseModel):
    criado_em: datetime
    ultima_categoria: str | None = None
    historico: list[ConversationMessage] = Field(default_factory=list)

    model_config = ConfigDict(arbitrary_types_allowed=True)
