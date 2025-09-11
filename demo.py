#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo rápida do Agente Curador de Contexto Pessoal
"""

import os
from cli import AgenteCLI

def demo_rapida():
    """Demonstração rápida das funcionalidades principais"""
    print("🎬 DEMO DO AGENTE CURADOR DE CONTEXTO PESSOAL")
    print("=" * 60)
    
    # Verifica API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  ATENÇÃO: API Key não configurada!")
        print("Configure primeiro com:")
        print("  $env:GOOGLE_API_KEY='sua_chave_do_gemini'")
        print("\nOu obtenha uma API key em:")
        print("  https://aistudio.google.com/app/apikey")
        
        api_key = input("\nDigite sua API Key agora (ou Enter para sair): ").strip()
        if not api_key:
            print("Demo cancelada. Configure a API key e tente novamente.")
            return
        
        # Define temporariamente para esta sessão
        os.environ['GOOGLE_API_KEY'] = api_key
    
    try:
        # Inicializa o agente
        print("🔧 Inicializando agente...")
        agente = AgenteCLI()
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")
        print("Verifique sua API key e conexão com a internet.")
        return
    
    # Demo 1: Adicionar memória
    print("\n📝 DEMO 1: Adicionando uma memória...")
    print("-" * 40)
    
    memoria_exemplo = """
    Reunião de planejamento 2025: decidimos focar em 3 objetivos principais:
    1) Crescer 30% em vendas até junho
    2) Lançar novo produto até março  
    3) Melhorar satisfação do cliente para 90%
    
    Principais bloqueios identificados:
    - Equipe pequena (precisamos contratar 2 pessoas)
    - Orçamento limitado para marketing
    - Sistema atual não suporta o volume esperado
    
    Deadline crítico: apresentação para investidores em 15 de fevereiro.
    """
    
    agente.adicionar_memoria(memoria_exemplo, "note", ["planejamento", "2025", "estrategia"])
    
    # Demo 2: Contexto
    print("\n📋 DEMO 2: Construindo contexto...")
    print("-" * 40)
    agente.onde_parei("planejamento")
    
    # Demo 3: Busca
    print("\n🔍 DEMO 3: Buscando memórias...")
    print("-" * 40)
    agente.buscar_memorias("vendas", 3)
    
    # Demo 4: Pergunta rápida
    print("\n❓ DEMO 4: Pergunta rápida...")
    print("-" * 40)
    agente.pergunta_rapida("Quais são meus maiores bloqueios atualmente?")
    
    print("\n🎉 DEMO CONCLUÍDA!")
    print("=" * 60)
    print("Para usar o agente completo:")
    print("• python cli.py                    # Menu interativo")
    print("• python cli.py --contexto tema   # Contexto específico")
    print("• python cli.py --reflexao geral  # Reflexão estratégica")

if __name__ == "__main__":
    demo_rapida()
