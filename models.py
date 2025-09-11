# -*- coding: utf-8 -*-
"""
Modelos de dados para o Agente Curador de Contexto Pessoal
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import uuid

class SourceMeta(BaseModel):
    source_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    kind: Literal["note", "email", "chat", "pdf", "task", "web"]
    created_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = []

class MemoryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    meta: SourceMeta
    # tipos de memória extraídos do conteúdo
    facts: List[str] = []
    decisions: List[str] = []
    goals: List[str] = []           # metas declaradas/implícitas
    blockers: List[str] = []        # impedimentos
    questions: List[str] = []       # dúvidas abertas
    deadlines: List[str] = []       # datas extraídas normalizadas ISO
    sentiment: Optional[Literal["pos", "neu", "neg"]] = "neu"
    importance: int = Field(default=1, ge=1, le=5)  # 1-5 (heurística/LLM)
    summary: str = ""               # resumo humano de 1-2 linhas
    raw_content: str = ""           # conteúdo original para referência

class Reflection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: datetime = Field(default_factory=datetime.now)
    triggers: List[str]             # o que disparou a reflexão
    contradictions: List[str] = []
    nudges: List[str] = []          # lembretes/sugestões curtas
    deep_questions: List[str] = []  # perguntas de reflexão
    next_actions: List[str] = []    # próximos passos práticos (até 5)

class ContextPanel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: datetime = Field(default_factory=datetime.now)
    query: str
    where_stopped: List[str] = []   # "onde parei" (3 bullets)
    goals_deadlines: List[str] = [] # metas e prazos
    blockers_hypotheses: List[str] = [] # bloqueios e hipóteses
    next_actions: List[str] = []    # 3-5 próximas ações priorizadas

class Nudge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: datetime = Field(default_factory=datetime.now)
    type: Literal["goal_stalled", "contradiction", "deadline_approaching", "repeated_blocker"]
    message: str
    memory_ids: List[str] = []      # memórias que geraram o nudge
    priority: int = Field(default=1, ge=1, le=5)
    is_read: bool = False
