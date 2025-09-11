# 🚀 GUIA RÁPIDO - Agente Curador de Contexto Pessoal

> 📖 **Para documentação completa**, veja [README.md](README.md)  
> ⚡ **Para comandos essenciais**, veja [QUICK_START.md](QUICK_START.md)

## 📋 Configuração (2 minutos)

### 1. Verificar ambiente
```powershell
python setup.py --check
```

### 2. Configuração completa
```powershell
python setup.py
```
☝️ Este comando vai te guiar pela configuração da API key e testar tudo.

### 3. OU configurar manualmente
```powershell
# Obter API key em: https://aistudio.google.com/app/apikey
$env:GOOGLE_API_KEY="sua_chave_do_gemini"
```

## 🎬 Primeiros Passos (5 minutos)

### 1. Teste rápido
```powershell
python demo.py
```

### 2. Menu interativo
```powershell
python cli.py
```

### 3. Adicione sua primeira memória
```powershell
python cli.py --texto "Reunião importante amanhã sobre projeto X. Preciso preparar relatório até quinta-feira. Bloqueio: falta dados do time Y."
```

### 4. Veja onde você parou
```powershell
python cli.py --contexto "projeto"
```

## 🔥 Casos de Uso Poderosos

### 📝 Journal Inteligente
Cole suas reflexões diárias e deixe o agente detectar padrões, metas e bloqueios automaticamente.

### 📧 Inbox Zero
Cole e-mails importantes para extrair tarefas, prazos e decisões.

### 🎯 Gestão de Metas
O agente detecta quando metas ficam estagnadas e te nudgea.

### 🤔 Reflexão Estratégica
Analisa suas memórias e aponta contradições entre o que você fala e faz.

## 💡 Dicas Pro

### Tags Inteligentes
```powershell
# Use tags consistentes para melhor organização
python cli.py --texto "..." --tags "trabalho,urgente,projeto-x"
```

### Contextos Específicos
```powershell
# Diferentes contextos para diferentes áreas da vida
python cli.py --contexto "carreira"
python cli.py --contexto "saúde"
python cli.py --contexto "estudos"
```

### Reflexão Periódica
```powershell
# Reflexão semanal
python cli.py --reflexao "semana" 

# Reflexão mensal sobre carreira
python cli.py --reflexao "carreira"
```

### Nudges Proativos
```powershell
# Verifique nudges todo dia
python cli.py --nudges
```

## 🎯 Fluxo de Trabalho Recomendado

### Manhã (2 min)
1. `python cli.py --nudges` - Ver lembretes
2. `python cli.py --contexto "hoje"` - Planejar o dia

### Durante o Dia
- Cole anotações de reuniões, e-mails importantes, insights
- Use `python cli.py --pergunta "..."` para consultas rápidas

### Fim de Semana (10 min)
- `python cli.py --reflexao "semana"` - Reflexão estratégica
- Revisar contradições e ajustar rumo

## 🔧 Arquivos Importantes

- `cli.py` - Interface principal
- `demo.py` - Demonstração rápida
- `config.py` - Configurações (ajuste conforme necessário)
- `README.md` - Documentação completa

## 🆘 Solução de Problemas

### Erro de API Key
```powershell
$env:GOOGLE_API_KEY="sua_chave_do_gemini"
```

### Erro de Dependências
```powershell
pip install chromadb langchain-google-genai langchain-chroma
```

### Performance Lenta
- Reduza `MAX_MEMORIES_CONTEXT` no `config.py`
- Use tags mais específicas para busca

## 🎉 Você está pronto!

O agente aprende com suas memórias e fica mais inteligente com o tempo. Quanto mais você usar, melhor ele entende seus padrões e pode te ajudar.
