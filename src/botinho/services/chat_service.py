"""Business logic for conversations and Gemini integration."""

from __future__ import annotations

import logging
import re
import textwrap
from datetime import UTC, datetime
from inspect import isawaitable
from time import monotonic
from typing import Any
from uuid import uuid4

from ..knowledge_base import CATEGORY_KEYWORDS, KNOWLEDGE_BASE, SYNONYMS
from ..models import ConversationData, ConversationMessage

try:
    from google import genai
    from google.genai import types as genai_types
except ImportError:  # pragma: no cover
    genai = None
    genai_types = None


# -- System instruction --------------------------------------------------------
_SYSTEM_INSTRUCTION = textwrap.dedent("""\
    Você é o Botinho, assistente virtual corporativo inteligente e prestativo.

    Você ajuda com qualquer dúvida do usuário, especialmente:
    - Políticas e procedimentos da empresa
    - Suporte técnico de TI (redes, hardware, software, Windows, impressoras, etc.)
    - Dúvidas gerais do ambiente de trabalho

    Como se comportar:
    - Responda em português do Brasil, de forma natural, clara e amigável.
    - Mantenha o fio da conversa: use o contexto do histórico para entender o que
      o usuário está perguntando sem pedir para repetir.
    - Quando pedirem mais detalhes, expanda com passos numerados e dicas práticas.
    - Use a base de conhecimento corporativo quando disponível, mas complemente
      com seu próprio conhecimento técnico quando necessário.
    - Seja proativo: se souber de algo relevante além do que foi perguntado, mencione.
    - Respostas curtas para perguntas simples, detalhadas para pedidos de explicação.
""")

_GENERATION_CONFIG: dict[str, Any] = {
    "temperature": 0.7,
    "top_p": 0.95,
    "max_output_tokens": 1024,
}


class GeminiClient:
    def __init__(self, api_key: str, model_name: str) -> None:
        self.model_name = model_name
        self._fallback_models = self._build_model_candidates(model_name)
        self._model_index = 0
        self._has_api_key = bool(api_key)
        self._has_sdk = bool(genai)
        self.available = bool(self._has_api_key and self._has_sdk)
        self._client = None

        if self.available:
            self._client = genai.Client(api_key=api_key)

    @staticmethod
    def _build_model_candidates(primary_model: str) -> list[str]:
        candidates = [
            primary_model,
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",
        ]
        deduped: list[str] = []
        seen: set[str] = set()
        for candidate in candidates:
            normalized = (candidate or "").strip().lower().replace("lastest", "latest")
            if normalized and normalized not in seen:
                seen.add(normalized)
                deduped.append(normalized)
        return deduped or ["gemini-2.0-flash"]

    def try_next_model(self) -> bool:
        if self._model_index >= len(self._fallback_models) - 1:
            return False
        self._model_index += 1
        self.model_name = self._fallback_models[self._model_index]
        return True

    async def create_chat(self, history: list[Any]) -> Any:
        """Create an async Gemini chat session pre-loaded with history."""
        if not self.available or not self._client:
            if not self._has_api_key:
                reason = "configure GEMINI_API_KEY"
            elif not self._has_sdk:
                reason = "instale a dependência google-genai na venv"
            else:
                reason = "verifique a configuração do cliente Gemini"
            raise RuntimeError(
                f"Gemini indisponivel: {reason} para habilitar respostas de IA."
            )

        config = None
        if genai_types:
            config = genai_types.GenerateContentConfig(
                system_instruction=_SYSTEM_INSTRUCTION,
                **_GENERATION_CONFIG,
            )

        chat = self._client.aio.chats.create(
            model=self.model_name,
            config=config,
            history=history,
        )
        if isawaitable(chat):
            return await chat
        return chat


class ChatService:
    def __init__(self, model_client: GeminiClient, logger: logging.Logger | None = None) -> None:
        self.model_client = model_client
        self.logger = logger or logging.getLogger("botinho.chat")
        self.conversations: dict[str, ConversationData] = {}
        self._gemini_cooldown_until = 0.0
        self._gemini_cooldown_logged = False

    # -- Session management ----------------------------------------------------

    def get_or_create_conversation(self, session_id: str | None) -> tuple[str, ConversationData]:
        resolved = session_id or f"session_{uuid4()}"
        if resolved not in self.conversations:
            self.conversations[resolved] = ConversationData(criado_em=datetime.now(UTC))
        return resolved, self.conversations[resolved]

    # -- Category / knowledge helpers ------------------------------------------

    def detect_category(self, message: str) -> str:
        normalized = self._normalize(message)
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(keyword in normalized for keyword in keywords):
                return category
        for base_term, aliases in SYNONYMS.items():
            if any(alias in normalized for alias in aliases):
                if base_term == "senha":
                    return "procedimentos_ti"
                if base_term in {"wifi", "email", "impressora", "sistema_lento"}:
                    return "problemas_tecnicos"
        return "conversa_geral"

    def search_knowledge(self, message: str) -> str | None:
        normalized = self._normalize(message)
        for _cat, topics in KNOWLEDGE_BASE.items():
            for topic_key, topic_value in topics.items():
                if any(token in normalized for token in topic_key.split("_")):
                    return topic_value
                if topic_key == "reset_senha" and any(
                    alias in normalized for alias in SYNONYMS["senha"]
                ):
                    return topic_value
                if topic_key == "wifi" and any(
                    alias in normalized for alias in SYNONYMS["wifi"]
                ):
                    return topic_value
                if topic_key == "email_lento" and any(
                    alias in normalized for alias in SYNONYMS["email"]
                ):
                    return topic_value
        return None

    # -- Main conversation entry point -----------------------------------------

    async def converse(self, message: str, session_id: str | None = None) -> dict[str, Any]:
        session_id, conversation = self.get_or_create_conversation(session_id)
        category = self.detect_category(message)
        knowledge = self.search_knowledge(message)
        last_category = conversation.ultima_categoria
        continues_topic = bool(
            last_category and last_category == category and category != "conversa_geral"
        )

        response = await self._generate_response(message, knowledge, conversation)

        conversation.historico.append(
            ConversationMessage(
                usuario=message,
                bot=response,
                categoria=category,
                timestamp=datetime.now(UTC),
            )
        )
        conversation.historico = conversation.historico[-20:]
        conversation.ultima_categoria = category

        return {
            "response": response,
            "confidence": 0.9 if knowledge else 0.7,
            "context_found": bool(knowledge),
            "continues_topic": continues_topic,
            "session_id": session_id,
            "timestamp": datetime.now(UTC),
            "model": (
                self.model_client.model_name
                if self.model_client.available
                else "knowledge-base-fallback"
            ),
        }

    # -- Response generation ---------------------------------------------------

    def _build_gemini_history(self, conversation: ConversationData) -> list[Any]:
        """Convert stored history to Gemini Content objects."""
        if not genai_types:
            return []
        history = []
        for entry in conversation.historico[-10:]:
            history.append(
                genai_types.Content(
                    role="user",
                    parts=[genai_types.Part.from_text(text=entry.usuario)],
                )
            )
            history.append(
                genai_types.Content(
                    role="model",
                    parts=[genai_types.Part.from_text(text=entry.bot)],
                )
            )
        return history

    async def _generate_response(
        self,
        message: str,
        knowledge: str | None,
        conversation: ConversationData,
    ) -> str:
        user_turn = message
        if knowledge:
            user_turn = (
                f"{message}\n\n"
                f"[Contexto da base de conhecimento corporativo: {knowledge}]"
            )

        if self._is_gemini_in_cooldown():
            return self._local_fallback(knowledge)

        for _attempt in range(4):
            try:
                history = self._build_gemini_history(conversation)
                chat = await self.model_client.create_chat(history)
                result = chat.send_message(message=user_turn)
                if isawaitable(result):
                    result = await result
                text = (result.text or "").strip()
                if text:
                    return text
            except Exception as exc:  # pragma: no cover
                error_text = str(exc)
                if self._is_quota_error(error_text):
                    if (
                        hasattr(self.model_client, "try_next_model")
                        and self.model_client.try_next_model()
                    ):
                        self.logger.warning(
                            "Quota no modelo atual. Tentando fallback de modelo Gemini: %s",
                            self.model_client.model_name,
                        )
                        continue

                    retry_seconds = self._extract_retry_seconds(error_text) or 60.0
                    retry_seconds = max(10.0, min(retry_seconds, 600.0))
                    self._gemini_cooldown_until = monotonic() + retry_seconds
                    self._gemini_cooldown_logged = False
                    self.logger.warning(
                        "Quota Gemini excedida. Fallback local por %.0fs. erro=%s",
                        retry_seconds,
                        error_text,
                    )
                    break

                if (
                    self._is_not_found_error(error_text)
                    and hasattr(self.model_client, "try_next_model")
                    and self.model_client.try_next_model()
                ):
                    self.logger.warning(
                        "Modelo Gemini inválido ou indisponível. Tentando fallback: %s",
                        self.model_client.model_name,
                    )
                    continue

                self.logger.warning(
                    "Falha ao consultar Gemini. Usando fallback local. erro=%s", error_text
                )
                break

        return self._local_fallback(knowledge)

    def _is_gemini_in_cooldown(self) -> bool:
        remaining = self._gemini_cooldown_until - monotonic()
        if remaining > 0:
            if not self._gemini_cooldown_logged:
                self.logger.info(
                    "Gemini temporariamente desativado por quota (%.0fs restantes). "
                    "Usando fallback local.",
                    remaining,
                )
                self._gemini_cooldown_logged = True
            return True

        self._gemini_cooldown_logged = False
        return False

    @staticmethod
    def _is_quota_error(error_text: str) -> bool:
        normalized = error_text.upper()
        return "RESOURCE_EXHAUSTED" in normalized or "QUOTA EXCEEDED" in normalized

    @staticmethod
    def _is_not_found_error(error_text: str) -> bool:
        normalized = error_text.upper()
        return "NOT_FOUND" in normalized or " IS NOT FOUND " in normalized

    @staticmethod
    def _extract_retry_seconds(error_text: str) -> float | None:
        for pattern in (r"retry in\s+([0-9]+(?:\.[0-9]+)?)s", r"'retryDelay':\s*'([0-9]+)s'"):
            match = re.search(pattern, error_text, flags=re.IGNORECASE)
            if match:
                return float(match.group(1))
        return None

    @staticmethod
    def _local_fallback(knowledge: str | None) -> str:
        if knowledge:
            return (
                f"{knowledge}\n\n"
                "Se quiser, posso detalhar os próximos passos para esse procedimento."
            )

        return (
            "Posso ajudar com políticas da empresa, procedimentos de TI "
            "e solução de problemas técnicos. "
            "Descreva seu cenário com mais detalhes para eu orientar com precisão."
        )

    @staticmethod
    def _normalize(text: str) -> str:
        normalized = text.lower().strip()
        return re.sub(r"\s+", " ", normalized)
