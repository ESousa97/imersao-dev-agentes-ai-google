# 🤖 Botinho - Chat AI com Google Gemini Flash 2.0

Uma assistente virtual inteligente desenvolvida com **Google Gemini Flash 2.0**, **FastAPI** e sistema de memória conversacional avançado.

<p align="center">
  <img src="https://raw.githubusercontent.com/ESousa97/imersao-dev-agentes-ai-google/master/img/Screenshot_1.png" 
       alt="Tela inicial do Botinho" width="600">
  <br><br>
  <img src="https://raw.githubusercontent.com/ESousa97/imersao-dev-agentes-ai-google/master/img/Screenshot_2.png" 
       alt="Conversa com Botinho" width="600">
</p>

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![Gemini](https://img.shields.io/badge/Google_Gemini-Flash_2.0-orange.svg)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)

## 🚀 Características Principais

- **🧠 IA Avançada**: Integração direta com Google Gemini Flash 2.0
- **💭 Memória Conversacional**: Sistema de contexto que mantém histórico entre interações
- **🎯 Base de Conhecimento**: Respostas especializadas para políticas empresariais e TI
- **⚡ Performance**: Arquitetura otimizada sem dependências pesadas
- **🌐 Interface Web**: Chat em tempo real com design responsivo
- **📊 Análise de Continuidade**: Detecta automaticamente mudanças de tópico
- **🔄 Gestão de Sessões**: Suporte a múltiplas conversas simultâneas

## 📋 Pré-requisitos

- **Python 3.8 ou superior**
- **Chave API do Google Gemini**
- **Conexão com internet**

## 🛠️ Instalação Rápida

### 1. Clone o repositório
```bash
git clone https://github.com/ESousa97/imersao-dev-agentes-ai-google.git
cd imersao-dev-agentes-ai-google
```

### 2. Instale as dependências
```bash
pip install fastapi uvicorn google-generativeai
```

### 3. Configure a chave API
Edite o arquivo `botinho.py` e substitua a chave API na linha 24:
```python
self.GEMINI_API_KEY = "SUA_CHAVE_API_AQUI"
```

### 4. Execute o Botinho
```bash
python botinho.py
```

### 5. Acesse a interface
Abra seu navegador em: **http://localhost:8000**

## 🎯 Como Usar

### Interface Web
1. Acesse `http://localhost:8000`
2. Digite sua mensagem no campo de chat
3. Pressione Enter ou clique em "Enviar"
4. O Botinho responderá mantendo o contexto da conversa

### API REST
```bash
# Enviar mensagem via API
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"mensagem": "Olá!", "session_id": "minha-sessao"}'
```

## 🏗️ Arquitetura

```
botinho.py
├── Config              # Configurações e base de conhecimento
├── Botinho (Classe)    # Motor principal da IA
│   ├── Memória         # Sistema de conversas
│   ├── Análise         # Continuidade de tópicos
│   └── Conhecimento    # Base de dados virtual
└── FastAPI             # Servidor web e API
```

## 📚 Base de Conhecimento

O Botinho possui conhecimento especializado em:

### 📋 Políticas da Empresa
- Horários de trabalho
- Política de férias
- Home office
- Equipamentos corporativos

### 🔧 Procedimentos de TI
- Reset de senhas
- Solicitação de acessos
- Backup de dados
- Configuração de VPN

### 🚨 Problemas Técnicos
- Conectividade Wi-Fi
- Performance de email
- Problemas com impressoras
- Otimização de sistema

## 🧠 Sistema de Memória

O Botinho utiliza um sistema avançado de memória que:
- **Mantém contexto** entre mensagens
- **Analisa continuidade** de tópicos automaticamente
- **Categoriza conversas** por assunto
- **Gerencia múltiplas sessões** simultaneamente

### Exemplo de Funcionamento
```
Usuário: "Como faço para resetar minha senha?"
Botinho: "Para resetar sua senha, acesse o portal..."

Usuário: "E se eu esquecer meu email?"
Botinho: "Continuando sobre o reset de senha, se você esqueceu o email..."
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```python
# No arquivo botinho.py
class Config:
    GEMINI_API_KEY = "sua_chave_aqui"
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    HOST = "0.0.0.0"
    PORT = 8000
```

### Personalizar Base de Conhecimento
Edite a seção `knowledge_base` no arquivo `botinho.py`:
```python
"sua_categoria": {
    "item_1": "Conteúdo da resposta...",
    "item_2": "Outro conteúdo..."
}
```

## 📊 Monitoramento

### Logs do Sistema
O Botinho gera logs detalhados:
- **INFO**: Operações normais
- **ERROR**: Problemas e falhas
- **DEBUG**: Informações técnicas

### Métricas de Performance
- Tempo de resposta da IA
- Análise de continuidade
- Gestão de sessões
- Uso da base de conhecimento

## 🔒 Segurança

- **Chave API**: Mantenha sua chave do Gemini segura
- **CORS**: Configurado para desenvolvimento local
- **Validação**: Entrada de dados sanitizada
- **Sessions**: IDs únicos para isolamento

## 🐛 Solução de Problemas

### Erro "Expecting value: line 1 column 1"
- **Causa**: Problema na análise JSON do Gemini
- **Solução**: Sistema automaticamente usa fallback

### Servidor não inicia
```bash
# Verificar se a porta está livre
netstat -ano | findstr :8000

# Usar porta alternativa
uvicorn botinho:app --port 8001
```

### API Key inválida
- Verifique se a chave do Gemini está correta
- Confirme se o serviço está ativo no Google Cloud

## 🚀 Próximas Funcionalidades

- [ ] Interface administrativa
- [ ] Múltiplos idiomas
- [ ] Integração com bancos de dados
- [ ] Analytics avançados
- [ ] Deploy em nuvem
- [ ] Autenticação de usuários

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/ESousa97/imersao-dev-agentes-ai-google/issues)
- **Documentação**: [docs/](docs/)

## 🙏 Agradecimentos

- Google Gemini Team pela API incrível
- FastAPI pela framework excepcional
- Comunidade Python pelo suporte

---

**Desenvolvido com ❤️ por [ESousa97](https://github.com/ESousa97)**

*Parte da Imersão Dev Agentes AI - Google*
