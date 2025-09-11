# -*- coding: utf-8 -*-
"""
Configurações do Agente Curador de Contexto Pessoal
"""

import os

class Config:
    # API e Modelos
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GEMINI_MODEL = "gemini-1.5-flash"
    EMBEDDING_MODEL = "models/text-embedding-004"
    
    # Banco de Dados
    SQLITE_PATH = "./agent_memory.db"
    CHROMA_PATH = "./chroma_mem"
    
    # Limites e Performance
    MAX_TEXT_LENGTH = 12000  # chars para curadoria
    MAX_MEMORIES_CONTEXT = 15  # memórias por contexto
    MAX_SEARCH_RESULTS = 10
    
    # Nudges e Proatividade
    GOAL_STALL_DAYS = 5      # dias sem movimento para nudge
    DEADLINE_WARNING_DAYS = 3 # dias antes do prazo para alerta
    REPEATED_BLOCKER_COUNT = 3 # vezes para considerar bloqueio repetido
    
    # Reflexão
    DEFAULT_REFLECTION_DAYS = 14
    MAX_NUDGES_PER_TYPE = 3
    
    # CLI
    DEFAULT_SEARCH_LIMIT = 10
    MENU_WIDTH = 60

# Prompts do sistema (centralizados para fácil ajuste)
PROMPTS = {
    "curadoria": """Você é um curador de contexto pessoal. Extraia do texto os campos específicos e responda APENAS com JSON válido no seguinte esquema:

{
  "facts": ["fato objetivo 1", "fato objetivo 2"],
  "decisions": ["decisão tomada 1", "decisão tomada 2"],
  "goals": ["meta declarada ou implícita 1", "meta 2"],
  "blockers": ["impedimento ou obstáculo 1", "bloqueio 2"],
  "questions": ["pergunta aberta 1", "dúvida 2"],
  "deadlines": ["YYYY-MM-DD formato ISO se houver data específica"],
  "sentiment": "pos" | "neu" | "neg",
  "importance": 1-5 (1=trivial, 5=crítico),
  "summary": "resumo de 1-2 linhas do conteúdo principal"
}

Regras:
- Extraia apenas o que está explícito ou claramente implícito
- Datas devem ser normalizadas para formato ISO YYYY-MM-DD
- Sentiment: pos=positivo/animado, neu=neutro/informativo, neg=frustração/problema
- Importance: baseie-se em urgência, impacto e emoção
- Summary: seja conciso mas informativo
- Se não houver conteúdo para algum campo, use lista vazia []""",

    "context_builder": """Você é um assistente de produtividade que constrói painéis de contexto. 

Baseado nas memórias fornecidas, construa um **Painel de Contexto** estruturado com:

1. **"Onde parei"** (3 bullets máximo): últimas ações, estado atual, momentum
2. **"Metas e prazos"**: objetivos ativos e datas importantes  
3. **"Bloqueios e hipóteses"**: obstáculos identificados e teorias sobre soluções
4. **"Próximas ações"** (3-5 itens): passos concretos priorizados por impacto

Responda APENAS com JSON no formato:
{
  "where_stopped": ["ação/estado 1", "ação/estado 2", "ação/estado 3"],
  "goals_deadlines": ["meta com prazo 1", "meta 2"],
  "blockers_hypotheses": ["bloqueio: hipótese 1", "bloqueio: hipótese 2"], 
  "next_actions": ["ação específica 1", "ação específica 2", "ação específica 3"]
}

Seja específico, acionável e direto. Evite generalidades.""",

    "reflection": """Você é um coach de reflexão estratégica. Analise o histórico de memórias e identifique:

**CONTRADIÇÕES**: Decisões/ações que conflitam com metas declaradas
**PERGUNTAS PROFUNDAS**: 3 questões que ajudam a esclarecer prioridades e direção  
**NUDGES PRÁTICOS**: 3 lembretes/sugestões diretas para destravar ou manter momentum
**PRÓXIMOS PASSOS**: Até 5 ações concretas prioritárias

Responda APENAS com JSON:
{
  "contradictions": ["contradição 1", "contradição 2"],
  "deep_questions": ["pergunta reflexiva 1", "pergunta 2", "pergunta 3"],
  "nudges": ["nudge prático 1", "nudge 2", "nudge 3"], 
  "next_actions": ["ação 1", "ação 2", "ação 3", "ação 4", "ação 5"]
}

Seja direto, específico e útil. Evite autoajuda genérica.""",

    "quick_answer": """Você é um assistente que usa as memórias pessoais do usuário para dar respostas diretas e úteis. Baseado nas memórias fornecidas, responda de forma direta e acionável em 2-3 parágrafos. Se não há informação suficiente, sugira que tipo de memória seria útil adicionar."""
}

# Emojis para interface
EMOJIS = {
    "tipos": {
        "note": "📝",
        "email": "📧", 
        "chat": "💬",
        "pdf": "📄",
        "task": "✅",
        "web": "🌐"
    },
    "nudges": {
        "goal_stalled": "😴",
        "contradiction": "⚠️",
        "deadline_approaching": "⏰",
        "repeated_blocker": "🔄"
    },
    "sentimentos": {
        "pos": "😊",
        "neu": "😐", 
        "neg": "😟"
    }
}

# Validação da configuração
def validate_config():
    """Valida se a configuração está correta"""
    if not Config.GOOGLE_API_KEY:
        return False, "GOOGLE_API_KEY não configurada"
    
    # Verifica se os diretórios podem ser criados
    try:
        import os
        os.makedirs(os.path.dirname(Config.SQLITE_PATH), exist_ok=True)
        os.makedirs(Config.CHROMA_PATH, exist_ok=True)
        return True, "Configuração válida"
    except Exception as e:
        return False, f"Erro ao criar diretórios: {e}"

if __name__ == "__main__":
    valid, msg = validate_config()
    print(f"Configuração: {msg}")
    if valid:
        print("✅ Pronto para usar!")
    else:
        print("❌ Configure a API key do Google Gemini")
