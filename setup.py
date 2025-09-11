#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração inicial do Agente Curador de Contexto Pessoal
"""

import os
import sys

def setup_inicial():
    """Configuração inicial do agente"""
    print("🔧 CONFIGURAÇÃO INICIAL DO AGENTE")
    print("=" * 50)
    
    # Verifica API key
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if api_key:
        print(f"✅ API Key encontrada: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("❌ API Key não encontrada")
        print("\n📋 Para obter uma API Key:")
        print("1. Acesse: https://aistudio.google.com/app/apikey")
        print("2. Clique em 'Create API Key'")
        print("3. Copie a chave gerada")
        
        api_key = input("\n🔑 Cole sua API Key aqui: ").strip()
        
        if not api_key:
            print("❌ API Key necessária para continuar")
            return False
        
        # Configura para a sessão atual
        os.environ['GOOGLE_API_KEY'] = api_key
        
        print("\n💡 Para configurar permanentemente no PowerShell:")
        print(f"  $env:GOOGLE_API_KEY='{api_key}'")
        print("\nOu adicione ao seu perfil do PowerShell:")
        print(f"  echo '$env:GOOGLE_API_KEY=\"{api_key}\"' >> $PROFILE")
    
    # Testa a conexão
    print("\n🔍 Testando conexão com o Google Gemini...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            api_key=api_key,
        )
        
        response = llm.invoke("Diga apenas 'OK' se você consegue me responder.")
        print(f"✅ Conexão OK: {response.content}")
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("Verifique sua API key e conexão com a internet")
        return False
    
    # Verifica dependências
    print("\n📦 Verificando dependências...")
    
    dependencias = [
        "langchain",
        "langchain_google_genai", 
        "langchain_community",
        "chromadb",
        "pydantic"
    ]
    
    faltando = []
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep}")
            faltando.append(dep)
    
    if faltando:
        print(f"\n⚠️  Instale as dependências faltantes:")
        print(f"  pip install {' '.join(faltando)}")
        return False
    
    # Testa inicialização completa
    print("\n🤖 Testando inicialização do agente...")
    
    try:
        # Importa apenas se todas as dependências estão OK
        from curadoria import Curador
        from db import DatabaseManager
        from agent import ContextAgent
        
        # Teste básico de inicialização
        curador = Curador(api_key)
        db = DatabaseManager(api_key=api_key)
        
        print("✅ Curadoria OK")
        print("✅ Banco de dados OK")
        print("✅ Agente OK")
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        return False
    
    print("\n🎉 CONFIGURAÇÃO COMPLETA!")
    print("=" * 50)
    print("Agora você pode usar:")
    print("• python demo.py          # Demo rápida")
    print("• python cli.py           # Menu completo")
    print("• python cli.py --help    # Ver todas as opções")
    
    return True

def verificar_ambiente():
    """Verifica se o ambiente está pronto"""
    print("🔍 VERIFICAÇÃO DO AMBIENTE")
    print("=" * 30)
    
    # Python
    print(f"Python: {sys.version}")
    
    # Diretório atual
    print(f"Diretório: {os.getcwd()}")
    
    # Arquivos principais
    arquivos_necessarios = [
        "models.py",
        "curadoria.py", 
        "db.py",
        "agent.py",
        "cli.py"
    ]
    
    print("\nArquivos principais:")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ❌ {arquivo}")
    
    # API Key
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"\nAPI Key: ✅ Configurada ({len(api_key)} chars)")
    else:
        print("\nAPI Key: ❌ Não configurada")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup do Agente")
    parser.add_argument("--check", action="store_true", help="Apenas verificar ambiente")
    
    args = parser.parse_args()
    
    if args.check:
        verificar_ambiente()
    else:
        success = setup_inicial()
        if not success:
            sys.exit(1)
