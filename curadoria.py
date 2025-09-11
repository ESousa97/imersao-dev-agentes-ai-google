# -*- coding: utf-8 -*-
"""
Módulo de Curadoria - Extrai estruturas do texto bruto usando LLM
"""

import json
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from models import MemoryItem, SourceMeta

class Curador:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            api_key=api_key,
        )
        
        self.curador_prompt = """Você é um curador de contexto pessoal. Extraia do texto os campos específicos e responda APENAS com JSON válido no seguinte esquema:

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
- Se não houver conteúdo para algum campo, use lista vazia []"""

    def curar_texto(self, texto: str, kind: str, tags: List[str] = None) -> Dict:
        """
        Processa texto bruto e extrai estruturas de memória
        """
        if tags is None:
            tags = []
            
        # Limita o texto para evitar tokens excessivos
        texto_limitado = texto[:12000] if len(texto) > 12000 else texto
        
        mensagem_usuario = f"""META: {tags}
SOURCE: {kind}
DATA:
```
{texto_limitado}
```"""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=self.curador_prompt),
                HumanMessage(content=mensagem_usuario)
            ])
            
            # Extrai JSON da resposta
            content = response.content.strip()
            
            # Remove markdown code blocks se presentes
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
                
            dados_extraidos = json.loads(content.strip())
            
            # Cria metadados
            meta = SourceMeta(
                kind=kind,
                tags=tags
            )
            
            # Cria o item de memória
            memory_item = MemoryItem(
                meta=meta,
                facts=dados_extraidos.get("facts", []),
                decisions=dados_extraidos.get("decisions", []),
                goals=dados_extraidos.get("goals", []),
                blockers=dados_extraidos.get("blockers", []),
                questions=dados_extraidos.get("questions", []),
                deadlines=dados_extraidos.get("deadlines", []),
                sentiment=dados_extraidos.get("sentiment", "neu"),
                importance=dados_extraidos.get("importance", 1),
                summary=dados_extraidos.get("summary", ""),
                raw_content=texto_limitado
            )
            
            return memory_item.model_dump()
            
        except json.JSONDecodeError as e:
            print(f"Erro ao parsear JSON da curadoria: {e}")
            print(f"Resposta recebida: {response.content}")
            # Retorna estrutura mínima em caso de erro
            meta = SourceMeta(kind=kind, tags=tags)
            memory_item = MemoryItem(
                meta=meta,
                summary=f"Erro na curadoria: {texto[:100]}...",
                raw_content=texto_limitado,
                importance=1
            )
            return memory_item.model_dump()
            
        except Exception as e:
            print(f"Erro inesperado na curadoria: {e}")
            meta = SourceMeta(kind=kind, tags=tags)
            memory_item = MemoryItem(
                meta=meta,
                summary=f"Erro na curadoria: {texto[:100]}...",
                raw_content=texto_limitado,
                importance=1
            )
            return memory_item.model_dump()

    def refinar_memoria(self, memory_item: Dict, contexto_adicional: str = "") -> Dict:
        """
        Refina uma memória existente com contexto adicional
        """
        prompt_refinamento = f"""Refine a memória existente com o contexto adicional:

MEMÓRIA ATUAL:
{json.dumps(memory_item, indent=2, ensure_ascii=False)}

CONTEXTO ADICIONAL:
{contexto_adicional}

Responda com JSON atualizado mantendo o mesmo esquema, incorporando novas informações relevantes."""

        try:
            response = self.llm.invoke([
                SystemMessage(content=self.curador_prompt),
                HumanMessage(content=prompt_refinamento)
            ])
            
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            dados_refinados = json.loads(content.strip())
            
            # Atualiza o item existente
            memory_item.update({
                "facts": dados_refinados.get("facts", memory_item.get("facts", [])),
                "decisions": dados_refinados.get("decisions", memory_item.get("decisions", [])),
                "goals": dados_refinados.get("goals", memory_item.get("goals", [])),
                "blockers": dados_refinados.get("blockers", memory_item.get("blockers", [])),
                "questions": dados_refinados.get("questions", memory_item.get("questions", [])),
                "deadlines": dados_refinados.get("deadlines", memory_item.get("deadlines", [])),
                "sentiment": dados_refinados.get("sentiment", memory_item.get("sentiment", "neu")),
                "importance": dados_refinados.get("importance", memory_item.get("importance", 1)),
                "summary": dados_refinados.get("summary", memory_item.get("summary", ""))
            })
            
            return memory_item
            
        except Exception as e:
            print(f"Erro no refinamento: {e}")
            return memory_item
