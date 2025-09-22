# 🚀 Guia de Instalação e Configuração - Botinho

## Índice
- [Instalação Rápida](#instalação-rápida)
- [Instalação Detalhada](#instalação-detalhada)
- [Configuração do Google Gemini](#configuração-do-google-gemini)
- [Configurações Avançadas](#configurações-avançadas)
- [Personalização](#personalização)
- [Solução de Problemas](#solução-de-problemas)

## Instalação Rápida

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Chave API do Google Gemini

### Comando único
```bash
# Clone, instale e execute
git clone https://github.com/ESousa97/imersao-dev-agentes-ai-google.git && \
cd imersao-dev-agentes-ai-google && \
pip install fastapi uvicorn google-generativeai && \
echo "Configure sua API key no arquivo botinho.py e execute: python botinho.py"
```

## Instalação Detalhada

### 1. Preparação do Ambiente

#### Windows
```powershell
# Verificar Python
python --version

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências (opcional)
pip install virtualenv
```

#### Linux/macOS
```bash
# Verificar Python
python3 --version

# Atualizar pip
python3 -m pip install --upgrade pip

# Instalar dependências
sudo apt-get install python3-venv  # Ubuntu/Debian
```

### 2. Criação de Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv botinho-env

# Ativar ambiente
# Windows
botinho-env\Scripts\activate

# Linux/macOS
source botinho-env/bin/activate
```

### 3. Clone do Repositório

```bash
# Via HTTPS
git clone https://github.com/ESousa97/imersao-dev-agentes-ai-google.git

# Via SSH (se configurado)
git clone git@github.com:ESousa97/imersao-dev-agentes-ai-google.git

# Entrar no diretório
cd imersao-dev-agentes-ai-google
```

### 4. Instalação de Dependências

#### Dependências Mínimas
```bash
pip install fastapi uvicorn google-generativeai
```

#### Dependências Completas (desenvolvimento)
```bash
pip install fastapi uvicorn google-generativeai pytest black flake8
```

#### Via requirements.txt
```bash
# Criar requirements.txt
echo "fastapi>=0.68.0
uvicorn>=0.15.0
google-generativeai>=0.3.0" > requirements.txt

# Instalar
pip install -r requirements.txt
```

### 5. Verificação da Instalação

```bash
# Testar imports
python -c "import fastapi, uvicorn, google.generativeai; print('✅ Todas as dependências instaladas!')"

# Verificar versões
pip list | grep -E "(fastapi|uvicorn|google-generativeai)"
```

## Configuração do Google Gemini

### 1. Obter Chave API

1. **Acesse**: [Google AI Studio](https://aistudio.google.com/)
2. **Login**: Com sua conta Google
3. **Navegue**: API Keys → Create API Key
4. **Copie**: A chave gerada

### 2. Configurar no Projeto

#### Método 1: Edição Direta (Desenvolvimento)
```python
# Editar linha 24 do botinho.py
self.GEMINI_API_KEY = "SUA_CHAVE_AQUI"
```

#### Método 2: Variável de Ambiente (Recomendado)
```bash
# Windows
set GEMINI_API_KEY=sua_chave_aqui

# Linux/macOS
export GEMINI_API_KEY=sua_chave_aqui

# Permanente no Linux/macOS
echo 'export GEMINI_API_KEY=sua_chave_aqui' >> ~/.bashrc
source ~/.bashrc
```

#### Método 3: Arquivo .env
```bash
# Criar arquivo .env
echo "GEMINI_API_KEY=sua_chave_aqui" > .env

# Modificar botinho.py para ler .env
pip install python-dotenv
```

```python
# Adicionar no início do botinho.py
from dotenv import load_dotenv
load_dotenv()

# Modificar Config class
class Config:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
```

### 3. Testar Conexão

```bash
# Teste simples
python -c "
import google.generativeai as genai
genai.configure(api_key='SUA_CHAVE')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Olá')
print('✅ Gemini conectado:', response.text[:50])
"
```

## Configurações Avançadas

### 1. Configuração de Servidor

```python
# No final do botinho.py, modificar:
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0",    # Aceitar conexões externas
        port=8000,         # Porta personalizada
        reload=True,       # Auto-reload em desenvolvimento
        log_level="info"   # Nível de log
    )
```

### 2. Configuração de CORS

```python
# Para permitir domínios específicos
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://meusite.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. Configuração de Logging

```python
# Logging personalizado
import logging
from logging.handlers import RotatingFileHandler

# Configurar handler de arquivo
file_handler = RotatingFileHandler(
    'botinho.log', 
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

# Adicionar ao logger
logger = logging.getLogger("Botinho")
logger.addHandler(file_handler)
```

## Personalização

### 1. Modificar Base de Conhecimento

```python
# Editar config.knowledge_base em botinho.py
self.knowledge_base = {
    "sua_categoria": {
        "topico_1": "Sua resposta personalizada aqui",
        "topico_2": "Outra resposta personalizada"
    },
    # Manter categorias existentes ou removê-las
    "politicas_empresa": {
        # Seus dados específicos
    }
}
```

### 2. Personalizar Interface

#### CSS Customizado
```html
<!-- Adicionar no HTML da interface -->
<style>
:root {
    --primary-color: #your-color;
    --secondary-color: #your-secondary;
}

.chat-container {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}
</style>
```

#### Logos e Branding
```python
# Modificar HTML no método get_chat_interface()
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Seu Bot Personalizado</title>
    <link rel="icon" href="seu-favicon.ico">
```

### 3. Adicionar Funcionalidades

#### Comando de Status
```python
# Adicionar endpoint de status
@app.get("/status")
async def status():
    return {
        "status": "online",
        "versao": "1.0.0",
        "uptime": str(datetime.now() - start_time),
        "conversas_ativas": len(botinho.conversations)
    }
```

#### Histórico de Conversas
```python
@app.get("/api/historico/{session_id}")
async def get_historico(session_id: str):
    conversa = botinho.get_or_create_conversation(session_id)
    return {"historico": conversa["historico"]}
```

## Solução de Problemas

### Problemas de Instalação

#### 1. Erro: "pip não é reconhecido"
**Solução Windows**:
```powershell
# Reinstalar Python com pip
# Download: https://python.org
# Marcar: "Add Python to PATH"

# Ou instalar pip manualmente
python -m ensurepip --upgrade
```

#### 2. Erro: "Permission denied"
**Solução Linux/macOS**:
```bash
# Usar --user
pip install --user fastapi uvicorn google-generativeai

# Ou usar sudo (não recomendado)
sudo pip install fastapi uvicorn google-generativeai
```

#### 3. Conflitos de Dependências
```bash
# Limpar cache pip
pip cache purge

# Forçar reinstalação
pip install --force-reinstall fastapi uvicorn google-generativeai

# Usar ambiente virtual limpo
deactivate
rm -rf botinho-env
python -m venv botinho-env
source botinho-env/bin/activate  # Linux/macOS
# botinho-env\Scripts\activate   # Windows
```

### Problemas de Configuração

#### 1. API Key Inválida
```bash
# Verificar se a chave está correta
echo $GEMINI_API_KEY  # Linux/macOS
echo %GEMINI_API_KEY% # Windows

# Testar manualmente
python -c "
import google.generativeai as genai
try:
    genai.configure(api_key='SUA_CHAVE')
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('test')
    print('✅ API Key válida')
except Exception as e:
    print('❌ Erro:', e)
"
```

#### 2. Porta em Uso
```bash
# Verificar processo usando a porta
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000

# Usar porta alternativa
python botinho.py --port 8001
# Ou modificar diretamente no código
```

#### 3. Problemas de CORS
```javascript
// Testar no navegador (F12 → Console)
fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({mensagem: 'teste'})
})
.then(r => r.json())
.then(console.log)
.catch(console.error)
```

### Problemas de Performance

#### 1. Resposta Lenta
```python
# Adicionar timeout ao Gemini
import google.generativeai as genai

# Configurar timeout (implementação futura)
genai.configure(
    api_key=self.GEMINI_API_KEY,
    timeout=30  # 30 segundos
)
```

#### 2. Memória Alta
```python
# Limpar conversas antigas
def limpar_conversas_antigas(self, horas=24):
    agora = datetime.now()
    sessoes_remover = []
    
    for session_id, conversa in self.conversations.items():
        if (agora - conversa["ultima_interacao"]).total_seconds() > horas * 3600:
            sessoes_remover.append(session_id)
    
    for session_id in sessoes_remover:
        del self.conversations[session_id]
```

### Scripts de Diagnóstico

#### Verificação Completa
```python
# diagnostico.py
import sys
import subprocess
import importlib

def verificar_python():
    print(f"Python: {sys.version}")
    return sys.version_info >= (3, 8)

def verificar_dependencias():
    deps = ["fastapi", "uvicorn", "google.generativeai"]
    for dep in deps:
        try:
            mod = importlib.import_module(dep)
            print(f"✅ {dep}: {getattr(mod, '__version__', 'instalado')}")
        except ImportError:
            print(f"❌ {dep}: não instalado")
            return False
    return True

def verificar_porta():
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 8000))
        print("✅ Porta 8000: disponível")
        return True
    except OSError:
        print("❌ Porta 8000: em uso")
        return False

if __name__ == "__main__":
    print("🔍 Diagnóstico do Botinho")
    print("-" * 30)
    
    checks = [
        verificar_python(),
        verificar_dependencias(),
        verificar_porta()
    ]
    
    if all(checks):
        print("\n✅ Sistema pronto para executar o Botinho!")
    else:
        print("\n❌ Problemas encontrados. Verifique os itens acima.")
```

---

**📞 Suporte**: Para problemas não resolvidos, abra uma [issue no GitHub](https://github.com/ESousa97/imersao-dev-agentes-ai-google/issues)