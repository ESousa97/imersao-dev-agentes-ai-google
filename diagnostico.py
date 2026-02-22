#!/usr/bin/env python3
"""
🔍 Script de Diagnóstico - Botinho
Verifica se o ambiente está configurado corretamente
"""

import importlib
import os
import socket
import subprocess
import sys
from datetime import datetime


def print_header():
    """Cabeçalho do diagnóstico"""
    print("🤖 BOTINHO - DIAGNÓSTICO DO SISTEMA")
    print("=" * 50)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Plataforma: {sys.platform}")
    print("-" * 50)

def verificar_python():
    """Verifica versão do Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    print(f"   Versão: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 8):
        print("   ✅ Python versão adequada")
        return True
    else:
        print("   ❌ Python 3.8+ necessário")
        return False

def verificar_pip():
    """Verifica se pip está disponível"""
    print("\n📦 Verificando pip...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ pip disponível: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ pip não encontrado")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao verificar pip: {e}")
        return False

def verificar_dependencias():
    """Verifica dependências principais"""
    print("\n📚 Verificando dependências...")
    
    dependencias = {
        "fastapi": "Framework web",
        "uvicorn": "Servidor ASGI",
        "google.generativeai": "API Google Gemini"
    }
    
    status = True
    for dep, desc in dependencias.items():
        try:
            mod = importlib.import_module(dep)
            version = getattr(mod, '__version__', 'N/A')
            print(f"   ✅ {dep}: {version} ({desc})")
        except ImportError:
            print(f"   ❌ {dep}: NÃO INSTALADO ({desc})")
            status = False
    
    return status

def verificar_porta():
    """Verifica se a porta 8000 está disponível"""
    print("\n🌐 Verificando porta 8000...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 8000))
        print("   ✅ Porta 8000 disponível")
        return True
    except OSError:
        print("   ⚠️  Porta 8000 em uso (pode ser o próprio Botinho)")
        return True  # Não é um erro crítico

def verificar_arquivos():
    """Verifica arquivos principais"""
    print("\n📁 Verificando arquivos...")
    
    arquivos = [
        "botinho.py",
        "README.md",
        "requirements.txt",
        "src/botinho/main.py",
        "docs/setup.md",
        ".env.example",
    ]
    
    status = True
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - AUSENTE")
            status = False
    
    return status

def verificar_api_key():
    """Verifica se API key está configurada"""
    print("\n🔑 Verificando configuração da API...")
    
    # Verificar variável de ambiente
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        print("   ✅ GEMINI_API_KEY encontrada em variável de ambiente")
        return True
    
    print("   ⚠️  GEMINI_API_KEY não encontrada no ambiente")
    print("      A aplicação ainda executa em modo fallback de base de conhecimento")
    return True

def instalar_dependencias():
    """Oferece instalar dependências em falta"""
    print("\n🔧 SOLUÇÕES:")
    print("\n1. Para instalar dependências:")
    print("   pip install -r requirements.txt")
    print("\n2. Para configurar API Key:")
    print("   - Obtenha em: https://aistudio.google.com/")
    print("   - Configure no arquivo .env (copiado de .env.example)")
    print("   - Ou: set GEMINI_API_KEY=sua_chave (Windows)")
    print("   - Ou: export GEMINI_API_KEY=sua_chave (Linux/Mac)")
    print("\n3. Para executar o Botinho:")
    print("   python botinho.py")

def verificar_conectividade():
    """Testa conectividade básica"""
    print("\n🌍 Verificando conectividade...")
    try:
        import requests
        response = requests.get("https://aistudio.google.com", timeout=5)
        if response.status_code == 200:
            print("   ✅ Conectividade com Google AI Studio OK")
            return True
        else:
            print("   ⚠️  Problema de conectividade")
            return False
    except ImportError:
        print("   ⚠️  requests não instalado (teste ignorado)")
        return True
    except Exception as e:
        print(f"   ⚠️  Erro de conectividade: {e}")
        return False

def main():
    """Função principal"""
    print_header()
    
    checks = [
        verificar_python(),
        verificar_pip(),
        verificar_dependencias(),
        verificar_porta(),
        verificar_arquivos(),
        verificar_api_key(),
        verificar_conectividade()
    ]
    
    print("\n" + "="*50)
    
    if all(checks):
        print("🎉 DIAGNÓSTICO COMPLETO!")
        print("✅ Sistema pronto para executar o Botinho!")
        print("\n🚀 Próximos passos:")
        print("   python botinho.py")
        print("   Acesse: http://localhost:8000")
    else:
        print("⚠️  PROBLEMAS ENCONTRADOS")
        print("❌ Sistema precisa de ajustes")
        instalar_dependencias()
    
    print("\n📞 Suporte: https://github.com/ESousa97/imersao-dev-agentes-ai-google")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Diagnóstico interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("Entre em contato com o suporte")