# 🤖 Agente Clip Windows

Um agente de IA que centraliza tudo que você consome/produz (anotações, e-mails, chats, PDFs, tarefas) em **memórias estruturadas**, e usa essas memórias para **sugerir ações e reflexões** no momento certo.

## 📑 Índice

- [🚀 Configuração Inicial](#-configuração-inicial-2-minutos)
- [🎬 Primeiros Passos](#-primeiros-passos)
- [📖 Como Usar - Linha de Comando](#-como-usar---linha-de-comando)
- [✨ Funcionalidades Detalhadas](#-funcionalidades-detalhadas)
- [🎯 Casos de Uso Práticos](#-casos-de-uso-práticos)
- [🔧 Arquivos do Sistema](#-arquivos-do-sistema)
- [🛠️ Personalização](#️-personalização)
- [🔍 Solução de Problemas](#-solução-de-problemas)
- [🚀 Fluxo de Trabalho Recomendado](#-fluxo-de-trabalho-recomendado)
- [🎯 Próximos Passos](#-próximos-passos)

---

## 🚀 Configuração Inicial (2 minutos)

### 1. Verificar Ambiente
```powershell
python setup.py --check
```

### 2. Configuração Automática (Recomendado)
```powershell
python setup.py
```
Este comando te guia pela configuração da API key e testa tudo automaticamente.

### 3. Configuração Manual
```powershell
# 1. Obter API key em: https://aistudio.google.com/app/apikey
# 2. Configurar variável de ambiente
$env:GOOGLE_API_KEY="sua_chave_do_gemini"

# 3. Verificar se está funcionando
python demo.py
```

## 🎬 Primeiros Passos

### Demo Rápida (5 minutos)
```powershell
python demo.py
```
Demonstra todas as funcionalidades principais com dados de exemplo.

### Menu Interativo
```powershell
python cli.py
```
Interface completa com menu guiado para todas as funcionalidades.

## 📖 Como Usar - Linha de Comando

### 📝 Adicionando Memórias
```powershell
# Texto simples
python cli.py --texto "Reunião importante amanhã sobre projeto X"

# Com tipo e tags
python cli.py --texto "Email do cliente pedindo antecipação" --tipo "email" --tags "urgente,cliente,projeto"

# Importar arquivo
python cli.py --arquivo documento.txt --tipo "pdf" --tags "estudo,importante"
```

### 📋 Consultando Contexto ("Onde Parei")
```powershell
# Contexto geral
python cli.py --contexto "geral"

# Contexto específico
python cli.py --contexto "trabalho"
python cli.py --contexto "estudos"
python cli.py --contexto "projeto X"
```

### 🤔 Reflexão Estratégica
```powershell
# Reflexão geral (últimos 14 dias)
python cli.py --reflexao "geral"

# Reflexão sobre tema específico
python cli.py --reflexao "carreira"
python cli.py --reflexao "vida pessoal"

# Período personalizado (via menu interativo)
python cli.py  # Escolha opção 3
```

### 🔍 Buscando Informações
```powershell
# Buscar memórias
python cli.py --buscar "projetos pendentes"
python cli.py --buscar "deadlines esta semana"

# Pergunta rápida
python cli.py --pergunta "O que tenho de importante para fazer hoje?"
python cli.py --pergunta "Quais são meus maiores bloqueios?"
```

### 🔔 Nudges Proativos
```powershell
# Verificar lembretes inteligentes
python cli.py --nudges
```

### 📊 Estatísticas
```powershell
# Ver estatísticas do banco de memórias
python cli.py --stats
```

### ❓ Ajuda
```powershell
# Ver todas as opções
python cli.py --help
```

## ✨ Funcionalidades Detalhadas

### 🧠 Curadoria Inteligente
O agente automaticamente extrai de qualquer texto:
- **Fatos**: Informações objetivas
- **Decisões**: Escolhas tomadas
- **Metas**: Objetivos declarados ou implícitos
- **Bloqueios**: Impedimentos e obstáculos
- **Perguntas**: Dúvidas abertas
- **Prazos**: Datas normalizadas (YYYY-MM-DD)
- **Sentiment**: Positivo/Neutro/Negativo
- **Importância**: Escala 1-5

### 📋 Painéis de Contexto
Cada consulta gera um painel estruturado:
```
🏃 ONDE PAREI:
• Última reunião: definiu 3 metas para Q1
• Pendência: aguardando aprovação do orçamento
• Progresso: 60% do projeto X concluído

🎯 METAS E PRAZOS:
• Lançar produto até março/2025
• Crescer vendas 30% até junho/2025
• Apresentação para investidores em 15/02

🚧 BLOQUEIOS E HIPÓTESES:
• Equipe pequena: contratar 2 pessoas
• Orçamento limitado: buscar parcerias

⚡ PRÓXIMAS AÇÕES:
1. Preparar apresentação para investidores
2. Iniciar processo de contratação
3. Definir estratégia de parcerias
```

### 🤔 Reflexão Estratégica
Analisa suas memórias e identifica:
- **Contradições**: Entre o que você fala e faz
- **Perguntas Profundas**: Para clarificar prioridades
- **Nudges Práticos**: Lembretes diretos
- **Próximos Passos**: Ações concretas

### 🔔 Nudges Proativos
O agente automaticamente detecta e te alerta sobre:
- **😴 Metas Estagnadas**: Sem movimento há 5+ dias
- **⚠️ Contradições**: Decisões conflitantes
- **⏰ Prazos Próximos**: Deadlines em 72h
- **🔄 Bloqueios Repetidos**: Obstáculos recorrentes

### 🔍 Busca Semântica
- Busca por significado, não só palavras-chave
- Embeddings do Google Gemini
- Resultados ordenados por relevância e importância

## 🎯 Casos de Uso Práticos

### 📅 Gestão Diária
```powershell
# Manhã: Ver o que fazer hoje
python cli.py --contexto "hoje"
python cli.py --nudges

# Durante o dia: Adicionar anotações
python cli.py --texto "Reunião com cliente: ele quer antecipar prazo para dezembro"

# Noite: Pergunta rápida
python cli.py --pergunta "O que consegui avançar hoje?"
```

### 📊 Planejamento Semanal
```powershell
# Segunda: Contexto da semana
python cli.py --contexto "esta semana"

# Sexta: Reflexão semanal
python cli.py --reflexao "semana"
```

### 🎯 Gestão de Projetos
```powershell
# Adicionar atualizações
python cli.py --texto "Projeto X: fase de testes concluída, encontrados 3 bugs críticos" --tags "projeto-x,bugs"

# Ver status
python cli.py --contexto "projeto X"

# Identificar bloqueios
python cli.py --pergunta "Quais são os principais riscos do projeto X?"
```

### 📧 Inbox Zero
```powershell
# Processar emails importantes
python cli.py --texto "Email do CEO: nova diretriz de home office, máximo 2 dias por semana" --tipo "email" --tags "politica,importante"

# Extrair tarefas
python cli.py --buscar "tarefas pendentes email"
```

### 📚 Gestão de Aprendizado
```powershell
# Adicionar insights de estudo
python cli.py --texto "Curso de Python: aprendi sobre decorators, mas ainda confuso com metaclasses" --tags "python,estudo"

# Ver progresso
python cli.py --contexto "estudos python"

# Identificar gaps
python cli.py --pergunta "O que ainda preciso aprender em Python?"
```

## 🔧 Arquivos do Sistema

### Core
- **`models.py`**: Estruturas de dados (Pydantic)
- **`curadoria.py`**: Extração inteligente via LLM
- **`db.py`**: Persistência híbrida SQLite + Chroma
- **`agent.py`**: Context Builder + Reflexão + Nudges
- **`cli.py`**: Interface de linha de comando

### Utilitários
- **`config.py`**: Configurações centralizadas
- **`setup.py`**: Configuração inicial guiada
- **`demo.py`**: Demonstração das funcionalidades
- **`teste_agente.py`**: Teste completo do sistema

### Documentação
- **`README.md`**: Este arquivo (documentação completa)
- **`GUIA_RAPIDO.md`**: Instruções condensadas
- **`.env.example`**: Template de configuração

## 🛠️ Personalização

### Ajustar Configurações
Edite `config.py` para personalizar:
```python
# Limites e Performance
MAX_TEXT_LENGTH = 12000  # chars para curadoria
MAX_MEMORIES_CONTEXT = 15  # memórias por contexto

# Nudges e Proatividade
GOAL_STALL_DAYS = 5      # dias sem movimento
DEADLINE_WARNING_DAYS = 3 # dias antes do prazo
```

### Personalizar Prompts
Modifique os prompts no `config.py` para ajustar o comportamento do agente.

### Adicionar Novos Tipos
Edite `models.py` para adicionar novos tipos de fonte:
```python
kind: Literal["note", "email", "chat", "pdf", "task", "web", "meeting"]
```

## 🔍 Solução de Problemas

### Erro de API Key
```powershell
# Verificar se está configurada
echo $env:GOOGLE_API_KEY

# Configurar novamente
$env:GOOGLE_API_KEY="sua_chave"

# Configuração permanente
echo '$env:GOOGLE_API_KEY="sua_chave"' >> $PROFILE
```

### Erro de Dependências
```powershell
# Reinstalar dependências
pip install -U langchain langchain-google-genai langchain-community chromadb pydantic langchain-chroma
```

### Performance Lenta
- Reduza `MAX_MEMORIES_CONTEXT` no `config.py`
- Use tags mais específicas para busca
- Limite o período de reflexão (7-14 dias)

### Banco Corrompido
```powershell
# Remover bancos e recomeçar
Remove-Item agent_memory.db
Remove-Item -Recurse chroma_mem
```

## 🚀 Fluxo de Trabalho Recomendado

### Setup Inicial (uma vez)
1. `python setup.py` - Configuração completa
2. `python demo.py` - Ver funcionalidades
3. Adicionar suas primeiras memórias

### Rotina Diária (5 minutos)
1. **Manhã**: `python cli.py --nudges` + `python cli.py --contexto "hoje"`
2. **Durante o dia**: Adicionar memórias importantes
3. **Noite**: `python cli.py --pergunta "O que avancei hoje?"`

### Rotina Semanal (15 minutos)
1. **Segunda**: `python cli.py --contexto "esta semana"`
2. **Sexta**: `python cli.py --reflexao "semana"`
3. Revisar contradições e ajustar rumo

### Rotina Mensal (30 minutos)
1. `python cli.py --reflexao "mês"`
2. `python cli.py --stats` - Ver estatísticas
3. Limpar memórias irrelevantes

## 🎯 Próximos Passos

### Funcionalidades Planejadas
- [ ] **OCR**: Processar PDFs e imagens automaticamente
- [ ] **Integração Email**: Importar emails diretamente
- [ ] **Calendário**: Sincronizar com Google Calendar
- [ ] **Web UI**: Interface web para facilitar uso
- [ ] **Relatórios**: Dashboards visuais de progresso
- [ ] **API**: Endpoints REST para integrações
- [ ] **Mobile**: App para captura rápida

### Melhorias Contínuas
- [ ] **Análise de Humor**: Detectar padrões emocionais
- [ ] **Previsões**: Antecipar bloqueios e oportunidades
- [ ] **Colaboração**: Compartilhar contextos com equipe
- [ ] **Automação**: Triggers para ferramentas externas

## 🏆 Diferenciais Únicos

✅ **Memória Explicável**: Cada insight mostra de onde veio  
✅ **Sempre Acionável**: 1-5 próximos passos em toda resposta  
✅ **Offline-first**: Dados locais, LLM só para raciocínio  
✅ **Self-aware**: O agente conhece seus padrões e te provoca  
✅ **Evolutivo**: Fica mais inteligente com o uso  
✅ **Privacidade**: Seus dados ficam no seu computador  

## 🎊 Transforme Informação em Ação

Com este agente, você nunca mais vai:
- ❌ Esquecer compromissos importantes
- ❌ Perder informações valiosas
- ❌ Repetir os mesmos erros
- ❌ Ficar estagnado sem saber o próximo passo
- ❌ Ter contradições entre metas e ações

E sempre vai:
- ✅ Saber exatamente onde parou em qualquer projeto
- ✅ Receber nudges quando algo importante estagnar
- ✅ Ter próximos passos claros e priorizados
- ✅ Identificar padrões e melhorar continuamente
- ✅ Manter foco no que realmente importa

**🚀 Comece agora: `python setup.py`**

---

## 💡 Exemplos Práticos de Comandos

### Cenário 1: Desenvolvedor trabalhando em múltiplos projetos
```powershell
# Adicionar atualizações de projetos
python cli.py --texto "Projeto A: API REST finalizada, faltam testes. Projeto B: bug crítico na autenticação descoberto." --tags "desenvolvimento,projetos"

# Ver status geral
python cli.py --contexto "desenvolvimento"

# Identificar gargalos
python cli.py --pergunta "Quais projetos precisam de atenção urgente?"
```

### Cenário 2: Estudante preparando certificação
```powershell
# Registrar progresso de estudo
python cli.py --texto "Estudei 3h hoje: decorators em Python dominados, mas async/await ainda confuso. Prova em 2 semanas." --tags "python,certificacao"

# Ver gaps de conhecimento
python cli.py --buscar "confuso ainda"

# Planejar estudos
python cli.py --contexto "certificacao"
```

### Cenário 3: Empreendedor gerenciando startup
```powershell
# Adicionar insights de reuniões
python cli.py --texto "Reunião com investidor: interessado, mas quer ver métricas de retenção melhoradas. Prazo: próxima reunião em 15 dias." --tags "investimento,metricas"

# Verificar lembretes
python cli.py --nudges

# Análise estratégica
python cli.py --reflexao "negócio"
```

### Cenário 4: Profissional em transição de carreira
```powershell
# Documentar networking
python cli.py --texto "Conversa com João (Tech Lead na empresa X): disse que vaga de Python dev vai abrir em breve. Enviar currículo semana que vem." --tags "networking,oportunidade"

# Acompanhar oportunidades
python cli.py --buscar "vagas oportunidades"

# Revisar estratégia
python cli.py --pergunta "Como está minha transição de carreira?"
```

---

## 📞 Suporte

- **Issues**: Abra um issue no repositório
- **Documentação**: Este README + `GUIA_RAPIDO.md`
- **Configuração**: Execute `python setup.py` para diagnóstico
- **Testes**: Execute `python demo.py` para verificar funcionamento

---

## 🎉 Pronto para Revolucionar sua Produtividade?

Este agente foi projetado para ser seu **segundo cérebro** - capturando, organizando e conectando suas informações de forma inteligente. Quanto mais você usar, mais poderoso ele se torna.

**Comece pequeno, pense grande:**
1. `python setup.py` - Configure em 2 minutos
2. `python demo.py` - Veja a mágica acontecer
3. `python cli.py` - Comece a usar no seu dia a dia

**Em uma semana você estará:**
- ✅ Capturando todas as informações importantes
- ✅ Recebendo nudges inteligentes
- ✅ Tendo clareza sobre próximos passos
- ✅ Identificando padrões que antes passavam despercebidos

**🚀 Transforme informação dispersa em ações focadas hoje mesmo!**
