# 🔌 API Reference - Botinho

## Índice
- [Visão Geral](#visão-geral)
- [Autenticação](#autenticação)
- [Endpoints](#endpoints)
- [Modelos de Dados](#modelos-de-dados)
- [Códigos de Status](#códigos-de-status)
- [Exemplos](#exemplos)
- [SDKs](#sdks)

## Visão Geral

**Base URL**: `http://localhost:8000`  
**Content-Type**: `application/json`  
**Versão**: `1.0.0`

A API do Botinho oferece endpoints para interações conversacionais com IA usando Google Gemini Flash 2.0.

## Autenticação

Atualmente não há autenticação necessária para desenvolvimento local. Para produção, recomenda-se implementar:

- API Keys
- JWT Tokens
- OAuth2

## Endpoints

### GET /

Retorna a interface web do chat.

**Response**: `text/html`

---

### POST /api/chat

Endpoint principal para conversas com o Botinho.

#### Request

**URL**: `/api/chat`  
**Method**: `POST`  
**Content-Type**: `application/json`

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `mensagem` | string | ✅ | Mensagem do usuário |
| `session_id` | string | ❌ | ID da sessão (gerado automaticamente se omitido) |

#### Request Body Example

```json
{
  "mensagem": "Como resetar minha senha?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Response

**Success (200)**:

```json
{
  "resposta": "Para resetar sua senha, acesse o portal...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-09-22T20:15:30.123456",
  "categoria": "procedimentos_ti",
  "usou_conhecimento": true,
  "analise_continuidade": {
    "continua_topico": false,
    "topico_anterior": null,
    "nova_categoria": "procedimentos_ti",
    "confianca": 0.85,
    "razao": "Nova pergunta sobre procedimentos de TI"
  }
}
```

**Error (400)**:

```json
{
  "detail": "Mensagem não pode estar vazia"
}
```

**Error (500)**:

```json
{
  "detail": "Erro interno do servidor: detalhes do erro"
}
```

---

### GET /health *(Futuro)*

Endpoint de health check para monitoramento.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-22T20:15:30.123456",
  "version": "1.0.0"
}
```

---

### GET /api/sessions *(Futuro)*

Lista sessões ativas.

**Response**:
```json
{
  "sessions": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "criada_em": "2025-09-22T20:00:00.000000",
      "ultima_interacao": "2025-09-22T20:15:30.123456",
      "contador_mensagens": 5
    }
  ]
}
```

---

### GET /api/sessions/{session_id}/history *(Futuro)*

Obtém histórico de uma sessão específica.

**Parameters**:
- `session_id` (path): ID da sessão

**Response**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "historico": [
    {
      "usuario": "Como resetar senha?",
      "bot": "Para resetar sua senha...",
      "timestamp": "2025-09-22T20:15:30.123456",
      "categoria": "procedimentos_ti"
    }
  ]
}
```

## Modelos de Dados

### ChatRequest

```typescript
interface ChatRequest {
  mensagem: string;        // Mensagem do usuário (obrigatório)
  session_id?: string;     // ID da sessão (opcional)
}
```

### ChatResponse

```typescript
interface ChatResponse {
  resposta: string;                    // Resposta do Botinho
  session_id: string;                  // ID da sessão
  timestamp: string;                   // ISO datetime
  categoria: string;                   // Categoria detectada
  usou_conhecimento: boolean;          // Se usou base de conhecimento
  analise_continuidade: AnalysisResult; // Análise de continuidade
}
```

### AnalysisResult

```typescript
interface AnalysisResult {
  continua_topico: boolean;    // Se continua o mesmo tópico
  topico_anterior: string;     // Descrição do tópico anterior
  nova_categoria: string;      // Nova categoria detectada
  confianca: number;          // Nível de confiança (0.0-1.0)
  razao: string;              // Explicação da análise
}
```

### ConversationHistory

```typescript
interface ConversationHistory {
  usuario: string;         // Mensagem do usuário
  bot: string;            // Resposta do bot
  timestamp: string;      // ISO datetime
  categoria: string;      // Categoria da interação
}
```

### Session

```typescript
interface Session {
  session_id: string;              // UUID da sessão
  criada_em: string;              // ISO datetime
  ultima_interacao: string;       // ISO datetime
  historico: ConversationHistory[]; // Array de interações
  ultima_categoria: string;        // Última categoria detectada
  contador_mensagens: number;      // Número de mensagens
}
```

## Códigos de Status

| Código | Descrição | Quando ocorre |
|--------|-----------|---------------|
| 200 | OK | Requisição processada com sucesso |
| 400 | Bad Request | Mensagem vazia ou dados inválidos |
| 404 | Not Found | Endpoint não encontrado |
| 405 | Method Not Allowed | Método HTTP não permitido |
| 500 | Internal Server Error | Erro no servidor ou API do Gemini |

## Exemplos

### cURL

#### Primeira conversa
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "mensagem": "Olá, como você funciona?"
     }'
```

#### Continuando conversa
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "mensagem": "Preciso de mais detalhes",
       "session_id": "550e8400-e29b-41d4-a716-446655440000"
     }'
```

### JavaScript/Fetch

```javascript
// Classe helper para API
class BotinhoAPI {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.sessionId = null;
  }

  async chat(mensagem) {
    try {
      const response = await fetch(`${this.baseURL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          mensagem,
          session_id: this.sessionId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      this.sessionId = data.session_id; // Manter sessão
      return data;
    } catch (error) {
      console.error('Erro na API:', error);
      throw error;
    }
  }
}

// Uso
const botinho = new BotinhoAPI();

// Primeira mensagem
const resposta1 = await botinho.chat("Qual o horário de trabalho?");
console.log(resposta1.resposta);

// Segunda mensagem (mantém sessão)
const resposta2 = await botinho.chat("E sobre home office?");
console.log(resposta2.resposta);
```

### Python

```python
import requests
import json
from typing import Optional, Dict, Any

class BotinhoAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id: Optional[str] = None
    
    def chat(self, mensagem: str) -> Dict[str, Any]:
        """Envia mensagem para o Botinho"""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "mensagem": mensagem
        }
        
        if self.session_id:
            payload["session_id"] = self.session_id
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Manter sessão
            self.session_id = data.get("session_id")
            
            return data
            
        except requests.exceptions.RequestException as e:
            return {"erro": str(e)}
    
    def reset_session(self):
        """Reset da sessão"""
        self.session_id = None

# Exemplo de uso
if __name__ == "__main__":
    botinho = BotinhoAPI()
    
    # Conversa
    resposta = botinho.chat("Como fazer backup?")
    print(f"Bot: {resposta['resposta']}")
    
    # Continuando
    resposta = botinho.chat("E se der erro?")
    print(f"Bot: {resposta['resposta']}")
    
    # Análise
    print(f"Categoria: {resposta['categoria']}")
    print(f"Usou conhecimento: {resposta['usou_conhecimento']}")
```

### Node.js

```javascript
const axios = require('axios');

class BotinhoAPI {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.sessionId = null;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  async chat(mensagem) {
    try {
      const payload = { mensagem };
      if (this.sessionId) {
        payload.session_id = this.sessionId;
      }

      const response = await this.client.post('/api/chat', payload);
      
      this.sessionId = response.data.session_id;
      return response.data;
      
    } catch (error) {
      if (error.response) {
        throw new Error(`API Error: ${error.response.status} - ${error.response.data.detail}`);
      } else {
        throw new Error(`Network Error: ${error.message}`);
      }
    }
  }

  resetSession() {
    this.sessionId = null;
  }
}

// Uso com async/await
async function exemplo() {
  const botinho = new BotinhoAPI();
  
  try {
    const resposta1 = await botinho.chat("Preciso resetar minha senha");
    console.log("Bot:", resposta1.resposta);
    
    const resposta2 = await botinho.chat("Não recebi o email");
    console.log("Bot:", resposta2.resposta);
    
  } catch (error) {
    console.error("Erro:", error.message);
  }
}

exemplo();
```

## SDKs

### Python SDK (Avançado)

```python
# botinho_sdk.py
import requests
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

class BotinhoSDK:
    def __init__(self, base_url: str = "http://localhost:8000", 
                 timeout: int = 30, debug: bool = False):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session_id: Optional[str] = None
        self.conversation_history: List[Dict] = []
        
        # Configurar logging
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
    
    def chat(self, mensagem: str, 
             new_session: bool = False) -> Dict[str, Any]:
        """
        Enviar mensagem para o Botinho
        
        Args:
            mensagem: Mensagem do usuário
            new_session: Se True, inicia nova sessão
            
        Returns:
            Resposta completa da API
        """
        if new_session:
            self.reset_session()
            
        url = f"{self.base_url}/api/chat"
        
        payload = {"mensagem": mensagem}
        if self.session_id:
            payload["session_id"] = self.session_id
        
        try:
            self.logger.debug(f"Enviando: {payload}")
            
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Atualizar estado
            self.session_id = data.get("session_id")
            
            # Adicionar ao histórico local
            self.conversation_history.append({
                "usuario": mensagem,
                "bot": data.get("resposta"),
                "timestamp": data.get("timestamp"),
                "categoria": data.get("categoria")
            })
            
            self.logger.debug(f"Resposta: {data}")
            return data
            
        except requests.exceptions.Timeout:
            return {"erro": "Timeout na requisição"}
        except requests.exceptions.ConnectionError:
            return {"erro": "Erro de conexão"}
        except requests.exceptions.HTTPError as e:
            return {"erro": f"Erro HTTP: {e.response.status_code}"}
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}"}
    
    def quick_chat(self, mensagem: str) -> str:
        """Versão simplificada que retorna apenas a resposta"""
        result = self.chat(mensagem)
        return result.get("resposta", result.get("erro", "Erro desconhecido"))
    
    def get_conversation_summary(self) -> Dict:
        """Resumo da conversa atual"""
        if not self.conversation_history:
            return {"mensagens": 0, "categorias": [], "session_id": None}
        
        categorias = list(set(h["categoria"] for h in self.conversation_history))
        
        return {
            "session_id": self.session_id,
            "mensagens": len(self.conversation_history),
            "categorias": categorias,
            "inicio": self.conversation_history[0]["timestamp"],
            "ultimo": self.conversation_history[-1]["timestamp"]
        }
    
    def reset_session(self):
        """Limpar sessão e histórico"""
        self.session_id = None
        self.conversation_history = []
        self.logger.debug("Sessão resetada")
    
    def export_conversation(self, format: str = "json") -> str:
        """Exportar conversa em diferentes formatos"""
        if format.lower() == "json":
            return json.dumps(self.conversation_history, indent=2)
        elif format.lower() == "txt":
            lines = []
            for h in self.conversation_history:
                lines.append(f"[{h['timestamp']}] Usuário: {h['usuario']}")
                lines.append(f"[{h['timestamp']}] Bot: {h['bot']}\n")
            return "\n".join(lines)
        else:
            raise ValueError("Formato suportado: 'json' ou 'txt'")

# Exemplo de uso avançado
if __name__ == "__main__":
    # Inicializar SDK
    sdk = BotinhoSDK(debug=True)
    
    # Conversa
    resposta1 = sdk.chat("Olá!")
    print(f"Bot: {sdk.quick_chat('Como resetar senha?')}")
    print(f"Bot: {sdk.quick_chat('E se não receber email?')}")
    
    # Resumo
    print("\nResumo:", sdk.get_conversation_summary())
    
    # Exportar
    print("\nConversa completa:")
    print(sdk.export_conversation("txt"))
```

## Rate Limiting *(Futuro)*

Para produção, recomenda-se implementar rate limiting:

```json
{
  "rate_limit": {
    "requests_per_minute": 60,
    "requests_per_hour": 1000
  },
  "headers": {
    "X-RateLimit-Limit": "60",
    "X-RateLimit-Remaining": "59",
    "X-RateLimit-Reset": "1634567890"
  }
}
```

## Webhooks *(Futuro)*

Para notificações em tempo real:

```json
{
  "webhook_url": "https://seu-servidor.com/webhook",
  "events": ["message_sent", "session_created"],
  "secret": "webhook_secret_key"
}
```

---

**📚 Documentação completa**: [docs/](./README.md)  
**🐛 Issues**: [GitHub Issues](https://github.com/ESousa97/imersao-dev-agentes-ai-google/issues)