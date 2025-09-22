# 📝 Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-09-22

### ✨ Adicionado
- Sistema de chat AI completo com Google Gemini Flash 2.0
- Interface web responsiva com design moderno
- Sistema de memória conversacional avançado
- Gestão de sessões com UUIDs únicos
- Base de conhecimento para políticas empresariais e TI
- Análise automática de continuidade de tópicos
- API REST completa para integração
- Sistema de logging detalhado
- Suporte a múltiplas conversas simultâneas
- Busca inteligente com sinônimos
- Middleware CORS configurado
- Tratamento robusto de erros JSON
- Documentação completa (README, guias técnicos, exemplos)

### 🏗️ Arquitetura
- FastAPI como framework web principal
- Integração direta com Google Gemini (sem LangChain)
- Arquitetura modular e escalável
- Sistema de configuração centralizado
- Estrutura de dados otimizada para memória

### 📚 Base de Conhecimento
- **Políticas da Empresa**: horários, férias, home office, equipamentos
- **Procedimentos de TI**: senhas, acessos, backup, VPN
- **Problemas Técnicos**: WiFi, email, impressoras, performance

### 🔧 Funcionalidades Técnicas
- Análise contextual com IA
- Categorização automática de conversas
- Extração inteligente de JSON das respostas
- Sistema de fallback para erros
- Histórico de conversas persistente
- Busca por palavras-chave e sinônimos

### 📖 Documentação
- README.md completo com instruções
- Guia de instalação detalhado
- Documentação técnica avançada
- Exemplos práticos de uso
- Referência completa da API
- Requirements.txt para dependências

## [0.2.0] - 2025-09-22

### ✨ Adicionado
- Sistema de memória conversacional
- Análise de continuidade de tópicos
- Gestão de sessões melhorada

### 🐛 Corrigido
- Erro de parsing JSON na análise de continuidade
- Problemas com f-strings contendo caracteres especiais
- Tratamento de erros melhorado

### 🔄 Modificado
- Prompts mais claros para o Gemini
- Extração robusta de JSON das respostas
- Logging mais detalhado para debug

## [0.1.0] - 2025-09-22

### ✨ Adicionado
- Versão inicial do Botinho
- Integração básica com Google Gemini Flash 2.0
- Interface web simples
- API básica de chat
- Base de conhecimento inicial

### 🐛 Conhecido
- Problemas de dependências com LangChain
- Conflitos de versão NumPy/Torch
- Parsing JSON instável

---

## Tipos de Mudanças

- **✨ Adicionado** para novas funcionalidades
- **🔄 Modificado** para mudanças em funcionalidades existentes
- **❌ Depreciado** para funcionalidades que serão removidas
- **🗑️ Removido** para funcionalidades removidas
- **🐛 Corrigido** para correção de bugs
- **🔒 Segurança** para correções de vulnerabilidades

## Roadmap Futuro

### [1.1.0] - Planejado
- [ ] Sistema de autenticação
- [ ] Persistência em banco de dados
- [ ] Interface administrativa
- [ ] Métricas e analytics
- [ ] Deploy automatizado

### [1.2.0] - Planejado  
- [ ] Suporte a múltiplos idiomas
- [ ] Integração com sistemas externos
- [ ] Webhooks e notificações
- [ ] Rate limiting
- [ ] Cache Redis

### [2.0.0] - Futuro
- [ ] Arquitetura microserviços
- [ ] Machine Learning personalizado
- [ ] Plugin system
- [ ] Mobile app
- [ ] Voice interface