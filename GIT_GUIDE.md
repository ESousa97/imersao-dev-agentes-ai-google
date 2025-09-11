# 🔒 Configuração de Segurança e Git

## 📁 Arquivos e Pastas Ignorados

O `.gitignore` está configurado para ignorar:

### 🔐 **Arquivos Sensíveis**
- `.env` - Variáveis de ambiente com API keys
- `api_keys.txt` - Chaves de API
- `secrets.json` - Configurações secretas
- `config.ini` - Configurações locais

### 🗄️ **Bancos de Dados e Cache**
- `agent_memory.db` - Banco SQLite com suas memórias pessoais
- `chroma_mem/` - Banco vetorial com embeddings
- `__pycache__/` - Cache do Python
- `*.cache` - Arquivos de cache

### 🔧 **Ambiente de Desenvolvimento**
- `.venv/` - Ambiente virtual Python
- `.vscode/` - Configurações do VS Code
- `*.log` - Arquivos de log

### 📄 **Arquivos Temporários**
- `*.tmp`, `*.temp` - Arquivos temporários
- `backup/` - Backups locais
- `imports/` - Documentos importados (podem ser sensíveis)

## ⚠️ Antes de Fazer Commit

### Verificar arquivos sensíveis
```powershell
# Ver o que será commitado
git status

# Verificar se não há API keys expostas
git diff --cached | Select-String -Pattern "AIza|sk-|pk_"
```

### Configuração recomendada do Git
```powershell
# Configurar informações pessoais
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"

# Configurações de segurança
git config --global core.autocrlf true  # Windows
git config --global init.defaultBranch main
```

## 🔄 Primeiro Commit

```powershell
# Adicionar arquivos principais (sem dados sensíveis)
git add .gitignore
git add *.py
git add *.md
git add .env.example

# Commit inicial
git commit -m "feat: Agente Curador de Contexto Pessoal - MVP completo

- Curadoria inteligente de texto para memórias estruturadas
- Painéis de contexto dinâmicos
- Reflexão estratégica com detecção de contradições  
- Nudges proativos baseados em padrões
- Busca semântica com embeddings
- CLI completa e configuração guiada"
```

## 🌐 Para Repositório Remoto

```powershell
# Conectar com repositório remoto
git remote add origin https://github.com/seu_usuario/agente-curador.git

# Push inicial
git push -u origin main
```

## 🚨 NUNCA Commitar

- ❌ Arquivo `.env` com API keys reais
- ❌ Banco `agent_memory.db` (contém suas memórias pessoais)
- ❌ Pasta `chroma_mem/` (embeddings das suas memórias)
- ❌ Arquivos com informações pessoais ou sensíveis
- ❌ Logs que podem conter dados pessoais

## ✅ SEMPRE Commitar

- ✅ Código fonte (*.py)
- ✅ Documentação (*.md)
- ✅ Arquivo `.gitignore`
- ✅ Arquivo `.env.example` (sem chaves reais)
- ✅ Configurações públicas

---

**🔒 Sua privacidade é fundamental! O agente funciona offline e seus dados ficam no seu computador.**
