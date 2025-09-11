# -*- coding: utf-8 -*-
"""
Agente Principal - Context Builder + Reflexão + Proatividade
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from models import ContextPanel, Reflection, Nudge
from db import DatabaseManager

class ContextAgent:
    def __init__(self, api_key: str, db_manager: DatabaseManager):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,  # Pouca criatividade para ser mais consistente
            api_key=api_key,
        )
        self.db = db_manager
        
        # Prompts do sistema
        self.context_builder_prompt = """Você é um assistente de produtividade que constrói painéis de contexto. 

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

Seja específico, acionável e direto. Evite generalidades."""

        self.reflection_prompt = """Você é um coach de reflexão estratégica. Analise o histórico de memórias e identifique:

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

Seja direto, específico e útil. Evite autoajuda genérica."""

    def construir_contexto(self, query: str, k: int = 12) -> Dict:
        """Constrói painel de contexto baseado na query"""
        
        # Busca memórias relevantes
        memorias_semanticas = self.db.buscar_memorias_semantica(query, k=k)
        memorias_recentes = self.db.buscar_memorias_filtros(days_back=7, importance_min=2, limit=8)
        
        # Combina e remove duplicatas
        todas_memorias = {m["id"]: m for m in memorias_semanticas + memorias_recentes}
        memorias_selecionadas = list(todas_memorias.values())[:15]  # Limita para não sobrecarregar
        
        if not memorias_selecionadas:
            return {
                "where_stopped": ["Nenhuma memória relacionada encontrada"],
                "goals_deadlines": [],
                "blockers_hypotheses": [],
                "next_actions": ["Adicione algumas memórias para começar"]
            }
        
        # Prepara resumo das memórias para o LLM
        memoria_texto = self._preparar_contexto_memorias(memorias_selecionadas)
        
        prompt_completo = f"""QUERY: {query}

MEMÓRIAS RELEVANTES:
{memoria_texto}"""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=self.context_builder_prompt),
                HumanMessage(content=prompt_completo)
            ])
            
            # Parse da resposta JSON
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            dados_painel = json.loads(content.strip())
            
            # Cria objeto ContextPanel
            painel = ContextPanel(
                query=query,
                where_stopped=dados_painel.get("where_stopped", []),
                goals_deadlines=dados_painel.get("goals_deadlines", []),
                blockers_hypotheses=dados_painel.get("blockers_hypotheses", []),
                next_actions=dados_painel.get("next_actions", [])
            )
            
            return painel.model_dump()
            
        except Exception as e:
            print(f"Erro ao construir contexto: {e}")
            return {
                "where_stopped": [f"Erro na análise: {str(e)[:100]}"],
                "goals_deadlines": [],
                "blockers_hypotheses": [],
                "next_actions": ["Tente refazer a consulta"]
            }

    def gerar_reflexao(self, escopo: str = "geral", days_back: int = 14) -> Dict:
        """Gera reflexão baseada nas memórias recentes"""
        
        # Busca memórias relevantes para reflexão
        if escopo == "geral":
            memorias = self.db.buscar_memorias_filtros(
                importance_min=2, 
                days_back=days_back, 
                limit=20
            )
        else:
            memorias = self.db.buscar_memorias_semantica(escopo, k=15)
        
        if not memorias:
            return {
                "contradictions": [],
                "deep_questions": ["Que áreas da minha vida merecem mais atenção?"],
                "nudges": ["Comece adicionando algumas memórias e metas"],
                "next_actions": ["Documente seus objetivos atuais"]
            }
        
        # Prepara dados para análise
        goals_history = []
        decisions_history = []
        blockers_history = []
        deadlines_approaching = []
        
        for memoria in memorias:
            goals_history.extend(memoria.get("goals", []))
            decisions_history.extend(memoria.get("decisions", []))
            blockers_history.extend(memoria.get("blockers", []))
            
            # Verifica deadlines próximos
            for deadline in memoria.get("deadlines", []):
                try:
                    deadline_date = datetime.fromisoformat(deadline)
                    days_until = (deadline_date - datetime.now()).days
                    if 0 <= days_until <= 7:
                        deadlines_approaching.append(f"{deadline}: {memoria.get('summary', 'N/A')}")
                except:
                    continue
        
        # Monta contexto para reflexão
        contexto_reflexao = f"""HISTÓRICO RECENTE ({days_back} dias):

METAS DECLARADAS:
{chr(10).join([f"- {goal}" for goal in set(goals_history)]) if goals_history else "- Nenhuma meta específica identificada"}

DECISÕES TOMADAS:
{chr(10).join([f"- {decision}" for decision in set(decisions_history)]) if decisions_history else "- Nenhuma decisão registrada"}

BLOQUEIOS IDENTIFICADOS:
{chr(10).join([f"- {blocker}" for blocker in set(blockers_history)]) if blockers_history else "- Nenhum bloqueio registrado"}

PRAZOS PRÓXIMOS (7 dias):
{chr(10).join([f"- {deadline}" for deadline in deadlines_approaching]) if deadlines_approaching else "- Nenhum prazo próximo"}

MEMÓRIAS DE ALTA IMPORTÂNCIA:
{chr(10).join([f"- {m.get('summary', 'N/A')}" for m in memorias if m.get('importance', 1) >= 4])[:1000]}"""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=self.reflection_prompt),
                HumanMessage(content=contexto_reflexao)
            ])
            
            # Parse da resposta
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            dados_reflexao = json.loads(content.strip())
            
            # Cria objeto Reflection
            triggers = [f"Análise de {len(memorias)} memórias", f"Escopo: {escopo}", f"Período: {days_back} dias"]
            
            reflexao = Reflection(
                triggers=triggers,
                contradictions=dados_reflexao.get("contradictions", []),
                nudges=dados_reflexao.get("nudges", []),
                deep_questions=dados_reflexao.get("deep_questions", []),
                next_actions=dados_reflexao.get("next_actions", [])
            )
            
            # Salva a reflexão
            reflexao_dict = reflexao.model_dump()
            self.db.salvar_reflexao(reflexao_dict)
            
            return reflexao_dict
            
        except Exception as e:
            print(f"Erro ao gerar reflexão: {e}")
            return {
                "contradictions": [],
                "deep_questions": ["O que está funcionando bem na minha rotina atual?"],
                "nudges": [f"Erro na análise: {str(e)[:100]}"],
                "next_actions": ["Revisar e reorganizar informações"]
            }

    def gerar_nudges_proativos(self) -> List[Dict]:
        """Gera nudges baseado em regras de proatividade"""
        nudges_gerados = []
        
        # Regra 1: Meta sem movimento (5+ dias)
        nudges_gerados.extend(self._nudge_metas_estagnadas())
        
        # Regra 2: Contradições recentes
        nudges_gerados.extend(self._nudge_contradicoes())
        
        # Regra 3: Prazos se aproximando
        nudges_gerados.extend(self._nudge_prazos_proximos())
        
        # Regra 4: Bloqueios repetidos
        nudges_gerados.extend(self._nudge_bloqueios_repetidos())
        
        # Salva nudges no banco
        for nudge_dict in nudges_gerados:
            self.db.salvar_nudge(nudge_dict)
        
        return nudges_gerados

    def _nudge_metas_estagnadas(self) -> List[Dict]:
        """Detecta metas sem progresso recente"""
        nudges = []
        
        # Busca metas dos últimos 30 dias
        memorias_com_metas = self.db.buscar_memorias_filtros(days_back=30, limit=100)
        
        # Agrupa metas por conteúdo similar
        metas_timeline = {}
        for memoria in memorias_com_metas:
            created_at = datetime.fromisoformat(memoria["meta"]["created_at"])
            for goal in memoria.get("goals", []):
                if goal not in metas_timeline:
                    metas_timeline[goal] = []
                metas_timeline[goal].append(created_at)
        
        # Verifica metas sem movimento recente
        cutoff_date = datetime.now() - timedelta(days=5)
        for meta, datas in metas_timeline.items():
            ultima_mencao = max(datas)
            if ultima_mencao < cutoff_date:
                nudge = Nudge(
                    type="goal_stalled",
                    message=f"A meta '{meta}' não teve movimento há {(datetime.now() - ultima_mencao).days} dias. Que tal 1 ação de 15 min para destravar?",
                    memory_ids=[],  # Could be enhanced to track specific memory IDs
                    priority=3
                )
                nudges.append(nudge.model_dump())
        
        return nudges[:3]  # Limita a 3 nudges deste tipo

    def _nudge_contradicoes(self) -> List[Dict]:
        """Detecta contradições entre decisões e metas"""
        nudges = []
        
        # Busca memórias recentes (7 dias)
        memorias_recentes = self.db.buscar_memorias_filtros(days_back=7, limit=50)
        
        # Extrai metas e decisões
        metas_recentes = []
        decisoes_recentes = []
        
        for memoria in memorias_recentes:
            metas_recentes.extend([(m, memoria["id"]) for m in memoria.get("goals", [])])
            decisoes_recentes.extend([(d, memoria["id"]) for d in memoria.get("decisions", [])])
        
        # Análise simples de contradição (palavras-chave opostas)
        palavras_conflito = [
            (["focar", "priorizar"], ["diversificar", "expandir"]),
            (["economizar", "cortar"], ["investir", "gastar"]),
            (["acelerar", "urgente"], ["pausar", "devagar"])
        ]
        
        for grupo_a, grupo_b in palavras_conflito:
            metas_a = [m for m, _ in metas_recentes if any(palavra in m.lower() for palavra in grupo_a)]
            decisoes_b = [d for d, _ in decisoes_recentes if any(palavra in d.lower() for palavra in grupo_b)]
            
            if metas_a and decisoes_b:
                nudge = Nudge(
                    type="contradiction",
                    message=f"Possível conflito: você priorizou '{metas_a[0][:50]}...' mas decidiu '{decisoes_b[0][:50]}...'. Qual vence esta semana?",
                    priority=4
                )
                nudges.append(nudge.model_dump())
        
        return nudges[:2]  # Limita contradições

    def _nudge_prazos_proximos(self) -> List[Dict]:
        """Detecta prazos se aproximando sem preparação"""
        nudges = []
        
        memorias = self.db.buscar_memorias_filtros(days_back=30, limit=100)
        
        for memoria in memorias:
            for deadline in memoria.get("deadlines", []):
                try:
                    deadline_date = datetime.fromisoformat(deadline)
                    days_until = (deadline_date - datetime.now()).days
                    
                    if 0 <= days_until <= 3:
                        # Verifica se há decisões/ações relacionadas recentes
                        summary = memoria.get("summary", "")
                        tem_preparo = any(
                            palavra in summary.lower() 
                            for palavra in ["preparar", "planejar", "organizar", "revisar"]
                        )
                        
                        if not tem_preparo:
                            nudge = Nudge(
                                type="deadline_approaching",
                                message=f"Prazo em {days_until} dia(s): {summary[:100]}. Hora de um checklist rápido?",
                                memory_ids=[memoria["id"]],
                                priority=5
                            )
                            nudges.append(nudge.model_dump())
                            
                except:
                    continue
        
        return nudges[:2]

    def _nudge_bloqueios_repetidos(self) -> List[Dict]:
        """Detecta bloqueios que se repetem"""
        nudges = []
        
        memorias = self.db.buscar_memorias_filtros(days_back=21, limit=100)
        
        # Conta bloqueios similares
        bloqueios_count = {}
        for memoria in memorias:
            for blocker in memoria.get("blockers", []):
                blocker_key = blocker.lower()[:50]  # Normaliza
                if blocker_key not in bloqueios_count:
                    bloqueios_count[blocker_key] = []
                bloqueios_count[blocker_key].append(memoria["id"])
        
        # Identifica bloqueios repetidos (3+ vezes)
        for blocker, memory_ids in bloqueios_count.items():
            if len(memory_ids) >= 3:
                nudge = Nudge(
                    type="repeated_blocker",
                    message=f"Bloqueio recorrente (3x): '{blocker}'. Hora de tentar uma abordagem diferente ou pedir ajuda?",
                    memory_ids=memory_ids,
                    priority=4
                )
                nudges.append(nudge.model_dump())
        
        return nudges[:2]

    def _preparar_contexto_memorias(self, memorias: List[Dict]) -> str:
        """Prepara texto resumido das memórias para o LLM"""
        contexto_linhas = []
        
        for memoria in memorias[:12]:  # Limita para não sobrecarregar
            data = memoria["meta"]["created_at"][:10]  # YYYY-MM-DD
            importance = "★" * memoria.get("importance", 1)
            summary = memoria.get("summary", "")
            
            linha = f"[{data}] {importance} {summary}"
            
            # Adiciona elementos estruturados se relevantes
            elementos = []
            if memoria.get("goals"):
                elementos.append(f"Metas: {', '.join(memoria['goals'][:2])}")
            if memoria.get("decisions"):
                elementos.append(f"Decisões: {', '.join(memoria['decisions'][:2])}")
            if memoria.get("blockers"):
                elementos.append(f"Bloqueios: {', '.join(memoria['blockers'][:2])}")
            if memoria.get("deadlines"):
                elementos.append(f"Prazos: {', '.join(memoria['deadlines'][:2])}")
            
            if elementos:
                linha += f" | {' | '.join(elementos)}"
            
            contexto_linhas.append(linha)
        
        return "\n".join(contexto_linhas)

    def buscar_resposta_rapida(self, pergunta: str) -> str:
        """Resposta rápida baseada em memórias relevantes"""
        memorias = self.db.buscar_memorias_semantica(pergunta, k=8)
        
        if not memorias:
            return "Não encontrei informações relevantes nas suas memórias. Que tal adicionar mais contexto?"
        
        contexto = self._preparar_contexto_memorias(memorias)
        
        prompt = f"""Baseado nas memórias do usuário, responda de forma direta e útil:

PERGUNTA: {pergunta}

MEMÓRIAS RELEVANTES:
{contexto}

Responda em 2-3 parágrafos, sendo específico e acionável. Se não há informação suficiente, sugira que tipo de memória seria útil adicionar."""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="Você é um assistente que usa as memórias pessoais do usuário para dar respostas diretas e úteis."),
                HumanMessage(content=prompt)
            ])
            
            return response.content.strip()
            
        except Exception as e:
            return f"Erro ao processar resposta: {e}"
