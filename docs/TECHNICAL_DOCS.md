# 📖 Documentação Técnica - Botinho

## Índice
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [API Reference](#api-reference)
- [Classes e Métodos](#classes-e-métodos)
- [Sistema de Memória](#sistema-de-memória)
- [Base de Conhecimento](#base-de-conhecimento)
- [Configurações](#configurações)
- [Deploy e Produção](#deploy-e-produção)

## Arquitetura do Sistema

### Visão Geral
O Botinho é construído em uma arquitetura modular com três componentes principais:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Interface     │◄──►│   FastAPI        │◄──►│   Google        │
│   Web/API       │    │   Backend        │    │   Gemini AI     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Sistema de     │
                       │   Memória        │
                       └──────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Base de        │
                       │   Conhecimento   │
                       └──────────────────┘
```

### Fluxo de Dados

1. **Input**: Usuário envia mensagem via interface web ou API
2. **Processamento**: Sistema analisa histórico e contexto
3. **Conhecimento**: Busca informações na base de dados
4. **IA**: Consulta o Gemini Flash 2.0 com contexto enriched
5. **Memória**: Armazena interação para futuras referências
6. **Output**: Retorna resposta contextualizada

## API Reference

### Endpoints Principais

#### `GET /`
**Descrição**: Interface web principal do chat
- **Método**: GET
- **Resposta**: HTML da interface
- **Content-Type**: text/html

#### `POST /api/chat`
**Descrição**: Endpoint principal para conversas
- **Método**: POST
- **Content-Type**: application/json

**Request Body**:
```json
{
  "mensagem": "string (obrigatório)",
  "session_id": "string (opcional)"
}
```

**Response Success (200)**:
```json
{
  "resposta": "string",
  "session_id": "uuid",
  "timestamp": "ISO datetime",
  "categoria": "string",
  "usou_conhecimento": "boolean",
  "analise_continuidade": {
    "continua_topico": "boolean",
    "topico_anterior": "string",
    "nova_categoria": "string",
    "confianca": "float"
  }
}
```

**Response Error (400/500)**:
```json
{
  "detail": "Mensagem de erro"
}
```

### Códigos de Status
- **200**: Sucesso
- **400**: Erro na requisição (mensagem vazia)
- **500**: Erro interno do servidor

## Classes e Métodos

### Classe `Config`
Centraliza todas as configurações do sistema.

```python
class Config:
    def __init__(self):
        self.GEMINI_API_KEY: str
        self.LOG_LEVEL: str
        self.knowledge_base: Dict
```

**Atributos**:
- `GEMINI_API_KEY`: Chave de acesso ao Google Gemini
- `LOG_LEVEL`: Nível de logging (DEBUG, INFO, WARNING, ERROR)
- `knowledge_base`: Dicionário com base de conhecimento

### Classe `Botinho`
Classe principal que gerencia toda a lógica da IA.

#### `__init__(self)`
Inicializa o Botinho com configurações do Gemini e sistema de logging.

#### `get_or_create_conversation(self, session_id: str) -> Dict`
**Descrição**: Obtém ou cria uma nova conversa para a sessão.

**Parâmetros**:
- `session_id` (str): ID único da sessão

**Retorna**:
- `Dict`: Objeto da conversa com histórico e metadados

**Estrutura da Conversa**:
```python
{
    "session_id": "uuid",
    "criada_em": "datetime",
    "ultima_interacao": "datetime", 
    "historico": [
        {
            "usuario": "mensagem do usuário",
            "bot": "resposta do bot",
            "timestamp": "datetime",
            "categoria": "categoria detectada"
        }
    ],
    "ultima_categoria": "string",
    "contador_mensagens": "int"
}
```

#### `analisar_continuidade(self, session_id: str, nova_mensagem: str) -> Dict`
**Descrição**: Analisa se o usuário está continuando o mesmo tópico ou mudando de assunto.

**Parâmetros**:
- `session_id` (str): ID da sessão
- `nova_mensagem` (str): Nova mensagem do usuário

**Retorna**:
```python
{
    "continua_topico": bool,
    "topico_anterior": str,
    "nova_categoria": str,
    "confianca": float,
    "razao": str
}
```

**Algoritmo**:
1. Recupera últimas 3 interações do histórico
2. Cria prompt estruturado para o Gemini
3. Analisa resposta e extrai JSON
4. Retorna análise ou fallback em caso de erro

#### `buscar_conhecimento(self, pergunta: str) -> Optional[str]`
**Descrição**: Busca informações na base de conhecimento usando palavras-chave e sinônimos.

**Parâmetros**:
- `pergunta` (str): Pergunta do usuário

**Retorna**:
- `str | None`: Informação encontrada ou None

**Algoritmo de Busca**:
1. Converte pergunta para lowercase
2. Itera por todas as categorias
3. Verifica correspondência por palavras-chave
4. Aplica sistema de sinônimos
5. Retorna primeira correspondência encontrada

#### `conversar(self, mensagem: str, session_id: str) -> Dict`
**Descrição**: Método principal para conversas com o usuário.

**Fluxo Completo**:
1. Análise de continuidade de tópico
2. Busca na base de conhecimento
3. Construção de contexto baseado no histórico
4. Consulta ao Gemini com prompt enriched
5. Processamento da resposta
6. Atualização da memória conversacional
7. Retorno da resposta estruturada

## Sistema de Memória

### Estrutura de Dados
O sistema utiliza um dicionário em memória para armazenar conversas:

```python
conversations = {
    "session_id_1": {
        "session_id": "uuid",
        "criada_em": datetime,
        "ultima_interacao": datetime,
        "historico": [...],
        "ultima_categoria": str,
        "contador_mensagens": int
    }
}
```

### Gestão de Sessões
- **IDs únicos**: Gerados automaticamente via UUID4
- **Persistência**: Mantido em memória durante execução
- **Limpeza**: Automática após inatividade (futura implementação)

### Análise de Contexto
O sistema analisa:
- **Continuidade de tópico**: Detecta mudanças de assunto
- **Categoria da conversa**: Classifica em 4 tipos principais
- **Confiança**: Score de 0.0 a 1.0 da análise
- **Histórico relevante**: Últimas 3 interações para contexto

## Base de Conhecimento

### Estrutura
Organizada em 3 categorias principais:

#### 1. Políticas da Empresa (`politicas_empresa`)
```python
{
    "horario_trabalho": "Horário de trabalho: 8h às 18h...",
    "ferias": "Política de férias: solicitar com 30 dias...",
    "home_office": "Home office: até 2 dias por semana...",
    "equipamentos": "Equipamentos corporativos: devolução..."
}
```

#### 2. Procedimentos de TI (`procedimentos_ti`)
```python
{
    "reset_senha": "Reset de senha: acesse o portal...",
    "solicitacao_acessos": "Solicitação de acessos: via ticket...",
    "backup": "Backup: automático às 2h da manhã...",
    "vpn": "VPN: obrigatória para acesso remoto..."
}
```

#### 3. Problemas Técnicos (`problemas_tecnicos`)
```python
{
    "wifi": "WiFi não funciona: reiniciar roteador...",
    "email_lento": "Email lento: limpar caixa de entrada...",
    "impressora": "Impressora: verificar papel, tinta...",
    "sistema_lento": "Sistema lento: fechar programas..."
}
```

### Sistema de Sinônimos
Mapeamento inteligente de termos similares:

```python
sinonimos = {
    'senha': ['password', 'login', 'acesso', 'logon'],
    'wifi': ['internet', 'rede', 'conexão', 'wi-fi'],
    'email': ['e-mail', 'correio', 'mensagem'],
    'impressora': ['printer', 'imprimir'],
    'sistema': ['computador', 'pc', 'máquina']
}
```

### Expansão da Base
Para adicionar nova categoria:

```python
config.knowledge_base["nova_categoria"] = {
    "item_1": "Resposta para item 1",
    "item_2": "Resposta para item 2"
}
```

## Configurações

### Variáveis de Ambiente
O sistema suporta configuração via variáveis de ambiente:

```bash
# Chave da API (recomendado)
export GEMINI_API_KEY="sua_chave_aqui"

# Nível de logging
export LOG_LEVEL="INFO"

# Configurações do servidor
export HOST="0.0.0.0"
export PORT="8000"
```

### Configuração de Logging
```python
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Produção: especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deploy e Produção

### Dependências de Produção
```bash
pip install fastapi uvicorn google-generativeai gunicorn
```

### Configuração do Gunicorn
```bash
gunicorn botinho:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "botinho:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variáveis de Ambiente - Produção
```bash
GEMINI_API_KEY=sua_chave_real
LOG_LEVEL=WARNING
CORS_ORIGINS=https://seudominio.com
```

### Monitoramento
- **Health Check**: Endpoint `/health` (implementar)
- **Métricas**: Integração com Prometheus (futuro)
- **Logs**: Centralização com ELK Stack (futuro)

### Segurança
- **API Key**: Nunca commitar no código
- **HTTPS**: Obrigatório em produção
- **Rate Limiting**: Implementar throttling
- **Validação**: Sanitização rigorosa de inputs

### Performance
- **Cache**: Redis para conversas (futuro)
- **Load Balancer**: Nginx ou AWS ALB
- **CDN**: Para assets estáticos
- **Database**: PostgreSQL para persistência

## Troubleshooting

### Problemas Comuns

#### 1. "Module not found: google.generativeai"
```bash
pip install google-generativeai
```

#### 2. "JSON decode error"
- Sistema implementa fallback automático
- Verificar logs para análise detalhada

#### 3. "Port already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

#### 4. API Key inválida
- Verificar no Google AI Studio
- Confirmar permissões do serviço

### Debug Mode
Para desenvolvimento, ative logs detalhados:

```python
# No início do botinho.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

**Última atualização**: 22 de Setembro de 2025
**Versão da documentação**: 1.0.0