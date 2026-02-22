# API Documentation

## Base URL
`http://localhost:8000`

## Endpoints

### GET /
Serves the chat web UI.

### GET /health
Health probe endpoint.

Example response:
```json
{
  "status": "ok",
  "version": "2.1.0",
  "environment": "development"
}
```

### POST /api/chat
Sends a user message and receives a bot response.

Request body (preferred):
```json
{
  "message": "Como resetar minha senha?",
  "session_id": "session_123"
}
```

Legacy request body still accepted for backward compatibility:
```json
{
  "mensagem": "Como resetar minha senha?",
  "session_id": "session_123"
}
```

Success response:
```json
{
  "response": "...",
  "confidence": 0.9,
  "context_found": true,
  "continues_topic": false,
  "session_id": "session_123",
  "timestamp": "2026-02-21T18:00:00.000000",
  "model": "gemini-2.0-flash-exp"
}
```

Error format:
```json
{
  "error": {
    "code": "validation_error",
    "message": "Payload inválido",
    "details": {}
  }
}
```

### GET /api/conversation/{session_id}
Returns session history for troubleshooting.

### GET /api/stats
Returns in-memory runtime stats.
