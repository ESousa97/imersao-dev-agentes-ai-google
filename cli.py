#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI para o Agente Curador de Contexto Pessoal
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict
import argparse

# Importa os módulos do agente
from curadoria import Curador
from db import DatabaseManager
from agent import ContextAgent

class AgenteCLI:
    def __init__(self):
        # Configura API key
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            print("⚠️  API Key do Google Gemini não encontrada!")
            print("Configure com: $env:GOOGLE_API_KEY='sua_chave'")
            print("Ou obtenha uma em: https://aistudio.google.com/app/apikey")
            self.api_key = input("\nDigite sua API Key do Google Gemini (ou Enter para sair): ").strip()
            if not self.api_key:
                print("❌ Saindo...")
                sys.exit(1)
        
        # Inicializa componentes
        print("🔧 Inicializando agente...")
        try:
            self.curador = Curador(self.api_key)
            self.db = DatabaseManager(api_key=self.api_key)
            self.agent = ContextAgent(self.api_key, self.db)
            print("✅ Agente pronto!\n")
        except Exception as e:
            print(f"❌ Erro ao inicializar agente: {e}")
            print("Verifique sua API key e conexão com a internet.")
            sys.exit(1)

    def adicionar_memoria(self, texto: str, tipo: str = "note", tags: List[str] = None):
        """Adiciona uma nova memória"""
        if tags is None:
            tags = []
            
        print(f"📝 Curando texto ({len(texto)} chars)...")
        
        # Cura o texto
        memoria_dict = self.curador.curar_texto(texto, tipo, tags)
        
        # Salva no banco
        memory_id = self.db.salvar_memoria(memoria_dict)
        
        print(f"✅ Memória salva: {memory_id}")
        print(f"📊 Resumo: {memoria_dict.get('summary', 'N/A')}")
        print(f"🎯 Importância: {memoria_dict.get('importance', 1)}/5")
        
        if memoria_dict.get('goals'):
            print(f"🎯 Metas: {', '.join(memoria_dict['goals'][:3])}")
        if memoria_dict.get('deadlines'):
            print(f"⏰ Prazos: {', '.join(memoria_dict['deadlines'])}")
        
        return memory_id

    def onde_parei(self, query: str = "geral"):
        """Mostra painel 'onde parei'"""
        print(f"🔍 Construindo contexto para: '{query}'...")
        
        painel = self.agent.construir_contexto(query)
        
        print("\n" + "="*60)
        print(f"📋 PAINEL DE CONTEXTO: {query.upper()}")
        print("="*60)
        
        print("\n🏃 ONDE PAREI:")
        for item in painel.get("where_stopped", []):
            print(f"  • {item}")
        
        print("\n🎯 METAS E PRAZOS:")
        for item in painel.get("goals_deadlines", []):
            print(f"  • {item}")
        
        print("\n🚧 BLOQUEIOS E HIPÓTESES:")
        for item in painel.get("blockers_hypotheses", []):
            print(f"  • {item}")
        
        print("\n⚡ PRÓXIMAS AÇÕES:")
        for i, item in enumerate(painel.get("next_actions", []), 1):
            print(f"  {i}. {item}")
        
        print("\n" + "="*60)

    def refletir(self, escopo: str = "geral", days: int = 14):
        """Gera reflexão estratégica"""
        print(f"🤔 Gerando reflexão sobre '{escopo}' ({days} dias)...")
        
        reflexao = self.agent.gerar_reflexao(escopo, days)
        
        print("\n" + "="*60)
        print("🧠 REFLEXÃO ESTRATÉGICA")
        print("="*60)
        
        if reflexao.get("contradictions"):
            print("\n⚠️  CONTRADIÇÕES DETECTADAS:")
            for item in reflexao["contradictions"]:
                print(f"  • {item}")
        
        print("\n❓ PERGUNTAS PROFUNDAS:")
        for i, item in enumerate(reflexao.get("deep_questions", []), 1):
            print(f"  {i}. {item}")
        
        print("\n💡 NUDGES PRÁTICOS:")
        for item in reflexao.get("nudges", []):
            print(f"  • {item}")
        
        print("\n🎯 PRÓXIMOS PASSOS:")
        for i, item in enumerate(reflexao.get("next_actions", []), 1):
            print(f"  {i}. {item}")
        
        print("\n" + "="*60)

    def verificar_nudges(self):
        """Verifica e mostra nudges pendentes"""
        print("🔔 Verificando nudges...")
        
        # Gera novos nudges
        novos_nudges = self.agent.gerar_nudges_proativos()
        if novos_nudges:
            print(f"✨ {len(novos_nudges)} novos nudges gerados")
        
        # Busca todos os nudges não lidos
        nudges = self.db.buscar_nudges_nao_lidos()
        
        if not nudges:
            print("✅ Nenhum nudge pendente!")
            return
        
        print(f"\n📢 {len(nudges)} NUDGES PENDENTES:")
        print("="*50)
        
        for i, nudge in enumerate(nudges, 1):
            priority_stars = "🔥" * nudge["priority"]
            tipo_emoji = {
                "goal_stalled": "😴",
                "contradiction": "⚠️",
                "deadline_approaching": "⏰",
                "repeated_blocker": "🔄"
            }.get(nudge["type"], "💡")
            
            print(f"\n{i}. {tipo_emoji} {priority_stars}")
            print(f"   {nudge['message']}")
            
            # Opção de marcar como lido
            resposta = input("   Marcar como lido? (s/N): ").lower()
            if resposta == 's':
                self.db.marcar_nudge_lido(nudge["id"])
                print("   ✅ Marcado como lido")

    def buscar_memorias(self, query: str, limite: int = 10):
        """Busca memórias"""
        print(f"🔍 Buscando: '{query}'...")
        
        memorias = self.db.buscar_memorias_semantica(query, k=limite)
        
        if not memorias:
            print("❌ Nenhuma memória encontrada")
            return
        
        print(f"\n📚 {len(memorias)} MEMÓRIAS ENCONTRADAS:")
        print("="*50)
        
        for i, memoria in enumerate(memorias, 1):
            data = memoria["meta"]["created_at"][:10]
            importance = "★" * memoria.get("importance", 1)
            tipo = memoria["meta"]["kind"]
            
            print(f"\n{i}. [{data}] {importance} ({tipo})")
            print(f"   {memoria.get('summary', 'Sem resumo')}")
            
            if memoria.get("goals"):
                print(f"   🎯 Metas: {', '.join(memoria['goals'][:2])}")
            if memoria.get("blockers"):
                print(f"   🚧 Bloqueios: {', '.join(memoria['blockers'][:2])}")

    def pergunta_rapida(self, pergunta: str):
        """Resposta rápida baseada em memórias"""
        print(f"❓ Processando: '{pergunta}'...")
        
        resposta = self.agent.buscar_resposta_rapida(pergunta)
        
        print("\n" + "="*60)
        print("💬 RESPOSTA:")
        print("="*60)
        print(f"\n{resposta}")
        print("\n" + "="*60)

    def estatisticas(self):
        """Mostra estatísticas do banco"""
        stats = self.db.estatisticas()
        
        print("\n📊 ESTATÍSTICAS DO AGENTE:")
        print("="*40)
        print(f"Total de memórias: {stats['total_memories']}")
        print(f"Nudges não lidos: {stats['unread_nudges']}")
        print(f"Tags únicas: {stats['total_tags']}")
        
        print("\nPor tipo:")
        for tipo, count in stats.get('by_type', {}).items():
            print(f"  {tipo}: {count}")
        
        print("\nPor importância:")
        for imp, count in stats.get('by_importance', {}).items():
            stars = "★" * int(imp)
            print(f"  {stars}: {count}")

    def importar_arquivo(self, caminho: str, tipo: str = "pdf", tags: List[str] = None):
        """Importa arquivo (texto simples por enquanto)"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            print(f"📁 Importando arquivo: {caminho}")
            return self.adicionar_memoria(conteudo, tipo, tags or [])
            
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {caminho}")
        except Exception as e:
            print(f"❌ Erro ao importar arquivo: {e}")

    def menu_interativo(self):
        """Menu principal interativo"""
        while True:
            print("\n" + "="*60)
            print("🤖 AGENTE CURADOR DE CONTEXTO PESSOAL")
            print("="*60)
            print("1. ➕ Adicionar memória")
            print("2. 📋 Onde parei? (contexto)")
            print("3. 🤔 Reflexão estratégica")  
            print("4. 🔔 Verificar nudges")
            print("5. 🔍 Buscar memórias")
            print("6. ❓ Pergunta rápida")
            print("7. 📊 Estatísticas")
            print("8. 📁 Importar arquivo")
            print("0. 🚪 Sair")
            print("="*60)
            
            try:
                opcao = input("Escolha uma opção: ").strip()
                
                if opcao == "0":
                    print("👋 Até logo!")
                    break
                    
                elif opcao == "1":
                    texto = input("\n📝 Cole seu texto: ")
                    if not texto.strip():
                        print("❌ Texto vazio!")
                        continue
                    
                    tipo = input("Tipo (note/email/chat/pdf/task/web) [note]: ").strip() or "note"
                    tags_input = input("Tags (separadas por vírgula): ").strip()
                    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
                    
                    self.adicionar_memoria(texto, tipo, tags)
                
                elif opcao == "2":
                    query = input("\n🔍 Contexto sobre (ou Enter para 'geral'): ").strip() or "geral"
                    self.onde_parei(query)
                
                elif opcao == "3":
                    escopo = input("\n🤔 Escopo da reflexão (ou Enter para 'geral'): ").strip() or "geral"
                    try:
                        days = int(input("Dias para analisar [14]: ").strip() or "14")
                    except ValueError:
                        days = 14
                    self.refletir(escopo, days)
                
                elif opcao == "4":
                    self.verificar_nudges()
                
                elif opcao == "5":
                    query = input("\n🔍 Buscar por: ")
                    if query.strip():
                        try:
                            limite = int(input("Limite de resultados [10]: ").strip() or "10")
                        except ValueError:
                            limite = 10
                        self.buscar_memorias(query, limite)
                
                elif opcao == "6":
                    pergunta = input("\n❓ Sua pergunta: ")
                    if pergunta.strip():
                        self.pergunta_rapida(pergunta)
                
                elif opcao == "7":
                    self.estatisticas()
                
                elif opcao == "8":
                    caminho = input("\n📁 Caminho do arquivo: ").strip()
                    if caminho:
                        tipo = input("Tipo [pdf]: ").strip() or "pdf"
                        tags_input = input("Tags: ").strip()
                        tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
                        self.importar_arquivo(caminho, tipo, tags)
                
                else:
                    print("❌ Opção inválida!")
                    
            except KeyboardInterrupt:
                print("\n👋 Saindo...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")

def main():
    parser = argparse.ArgumentParser(description="Agente Curador de Contexto Pessoal")
    parser.add_argument("--texto", help="Adicionar texto diretamente")
    parser.add_argument("--tipo", default="note", help="Tipo de fonte")
    parser.add_argument("--tags", help="Tags separadas por vírgula")
    parser.add_argument("--contexto", help="Mostrar contexto sobre tema")
    parser.add_argument("--reflexao", help="Gerar reflexão sobre tema")
    parser.add_argument("--buscar", help="Buscar memórias")
    parser.add_argument("--pergunta", help="Pergunta rápida")
    parser.add_argument("--nudges", action="store_true", help="Verificar nudges")
    parser.add_argument("--stats", action="store_true", help="Mostrar estatísticas")
    parser.add_argument("--arquivo", help="Importar arquivo")
    
    args = parser.parse_args()
    
    # Inicializa o agente
    agente = AgenteCLI()
    
    # Processa argumentos da linha de comando
    if args.texto:
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        agente.adicionar_memoria(args.texto, args.tipo, tags)
        
    elif args.contexto:
        agente.onde_parei(args.contexto)
        
    elif args.reflexao:
        agente.refletir(args.reflexao)
        
    elif args.buscar:
        agente.buscar_memorias(args.buscar)
        
    elif args.pergunta:
        agente.pergunta_rapida(args.pergunta)
        
    elif args.nudges:
        agente.verificar_nudges()
        
    elif args.stats:
        agente.estatisticas()
        
    elif args.arquivo:
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        agente.importar_arquivo(args.arquivo, args.tipo, tags)
        
    else:
        # Se não há argumentos, abre menu interativo
        agente.menu_interativo()

if __name__ == "__main__":
    main()
