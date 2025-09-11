#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o Agente Curador de Contexto Pessoal
"""

import os
import sys
from cli import AgenteCLI

def teste_completo():
    """Executa um teste completo do agente"""
    print("🧪 INICIANDO TESTE COMPLETO DO AGENTE")
    print("="*50)
    
    # Inicializa o agente
    agente = AgenteCLI()
    
    # Dados de teste
    memorias_teste = [
        {
            "texto": "Definir metas de estudo para 2025: preciso focar em Python, IA e desenvolvimento web. Deadline para começar curso: 15 de janeiro. Bloqueio atual: falta de tempo devido ao trabalho.",
            "tipo": "note",
            "tags": ["estudo", "metas", "2025"]
        },
        {
            "texto": "Reunião com o chefe hoje: decidimos que vou liderar o projeto X a partir de março. Preciso me preparar estudando gestão de projetos. Meta: terminar certificação PMP até maio.",
            "tipo": "note", 
            "tags": ["trabalho", "projeto", "carreira"]
        },
        {
            "texto": "Reflexão pessoal: sinto que estou disperso entre muitos objetivos. Quero focar mais em saúde, mas sempre priorizo trabalho. Talvez devesse acordar mais cedo para exercícios.",
            "tipo": "note",
            "tags": ["pessoal", "saude", "habitos"]
        },
        {
            "texto": "Email importante: cliente pediu para antecipar entrega do projeto Y para 20 de dezembro. Isso vai afetar meu planejamento de estudos. Preciso renegociar ou reorganizar prioridades.",
            "tipo": "email",
            "tags": ["urgente", "projeto", "cliente"]
        },
        {
            "texto": "Conversa com mentor: ele sugeriu que eu deveria especializar em uma área ao invés de tentar aprender tudo. Talvez focar só em IA seja melhor que dispersar entre web e IA.",
            "tipo": "chat",
            "tags": ["mentoria", "decisao", "foco"]
        }
    ]
    
    print("\n1️⃣ ADICIONANDO MEMÓRIAS DE TESTE...")
    memory_ids = []
    for i, mem in enumerate(memorias_teste, 1):
        print(f"\n   Memória {i}/5:")
        mem_id = agente.adicionar_memoria(mem["texto"], mem["tipo"], mem["tags"])
        memory_ids.append(mem_id)
    
    print("\n2️⃣ TESTANDO CONTEXTO 'ONDE PAREI'...")
    agente.onde_parei("estudo")
    
    print("\n3️⃣ TESTANDO REFLEXÃO ESTRATÉGICA...")
    agente.refletir("carreira e estudos", 30)
    
    print("\n4️⃣ TESTANDO GERAÇÃO DE NUDGES...")
    agente.verificar_nudges()
    
    print("\n5️⃣ TESTANDO BUSCA DE MEMÓRIAS...")
    agente.buscar_memorias("projetos", 5)
    
    print("\n6️⃣ TESTANDO PERGUNTA RÁPIDA...")
    agente.pergunta_rapida("Como devo priorizar entre estudos e trabalho?")
    
    print("\n7️⃣ MOSTRANDO ESTATÍSTICAS...")
    agente.estatisticas()
    
    print("\n✅ TESTE COMPLETO FINALIZADO!")
    print("="*50)
    print("O agente está funcionando! Agora você pode:")
    print("• Executar 'python cli.py' para o menu interativo")
    print("• Usar argumentos diretos como 'python cli.py --texto \"sua memória\"'")
    print("• Importar arquivos com 'python cli.py --arquivo caminho.txt'")

if __name__ == "__main__":
    teste_completo()
