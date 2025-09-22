# Botinho - Chat AI com Google Gemini Flash 2.0
# Versão simplificada e otimizada

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import uuid

# Web Framework
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Google Gemini API direto
import google.generativeai as genai

# Configuração
class Config:
    def __init__(self):
        self.GEMINI_API_KEY = "SUA_CHAVE_KEY_AQUI"
        self.LOG_LEVEL = "INFO"
        
        # Base de conhecimento virtual
        self.knowledge_base = {
            "politicas_empresa": {
                "horario_trabalho": "Horário de trabalho: 8h às 18h, segunda a sexta-feira",
                "ferias": "Política de férias: solicitar com 30 dias de antecedência via sistema",
                "home_office": "Home office: até 2 dias por semana com aprovação do gestor",
                "equipamentos": "Equipamentos corporativos: devolução obrigatória ao sair da empresa"
            },
            "procedimentos_ti": {
                "reset_senha": "Reset de senha: acesse o portal → 'Esqueci senha' → verificar email",
                "solicitacao_acessos": "Solicitação de acessos: via ticket no sistema interno",
                "backup": "Backup: automático às 2h da manhã, restore sob demanda",
                "vpn": "VPN: obrigatória para acesso remoto aos sistemas internos"
            },
            "problemas_tecnicos": {
                "wifi": "WiFi não funciona: reiniciar roteador, verificar cabos, contactar TI",
                "email_lento": "Email lento: limpar caixa de entrada, esvaziar lixeira",
                "impressora": "Impressora: verificar papel, tinta, reiniciar equipamento",
                "sistema_lento": "Sistema lento: fechar programas desnecessários, reiniciar PC"
            }
        }

config = Config()

# Configurar Gemini
genai.configure(api_key=config.GEMINI_API_KEY)

# Botinho - Assistant
class Botinho:
    def __init__(self):
        self.setup_logging()
        self.gemini = genai.GenerativeModel('gemini-2.0-flash-exp')
        # Sistema de memória conversacional
        self.conversations = {}  # session_id -> conversation_data
        self.logger.info("Botinho inicializado com Gemini Flash 2.0 e sistema de memória!")
        
    def setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("Botinho")
    
    def get_or_create_conversation(self, session_id: str) -> Dict:
        """Obtém ou cria uma nova conversa"""
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                "historico": [],
                "contexto_atual": None,
                "topico_atual": None,
                "ultima_categoria": None,
                "criado_em": datetime.now().isoformat()
            }
        return self.conversations[session_id]
    
    def adicionar_ao_historico(self, session_id: str, mensagem_usuario: str, resposta_bot: str, categoria: str = None):
        """Adiciona interação ao histórico"""
        conversa = self.get_or_create_conversation(session_id)
        conversa["historico"].append({
            "usuario": mensagem_usuario,
            "bot": resposta_bot,
            "categoria": categoria,
            "timestamp": datetime.now().isoformat()
        })
        
        # Manter apenas as últimas 10 interações para não sobrecarregar
        if len(conversa["historico"]) > 10:
            conversa["historico"] = conversa["historico"][-10:]
        
        # Atualizar contexto atual
        if categoria:
            conversa["ultima_categoria"] = categoria
    
    def analisar_continuidade(self, session_id: str, nova_mensagem: str) -> Dict:
        """Analisa se o usuário está continuando o assunto ou mudando de tópico"""
        conversa = self.get_or_create_conversation(session_id)
        
        if not conversa["historico"]:
            return {"continua_topico": False, "topico_anterior": None}
        
        # Pegar as últimas 3 interações para contexto
        historico_recente = conversa["historico"][-3:]
        
        # Criar prompt para o Gemini analisar continuidade
        newline = chr(10)
        historico_texto = newline.join([f"Usuário: {h['usuario']}{newline}Bot: {h['bot'][:200]}..." for h in historico_recente])
        
        prompt_analise = f"""
        Analise se o usuário está continuando o mesmo assunto ou mudando de tópico.
        
        HISTÓRICO RECENTE DA CONVERSA:
        {historico_texto}
        
        NOVA MENSAGEM DO USUÁRIO: {nova_mensagem}
        
        CATEGORIA ANTERIOR: {conversa.get('ultima_categoria', 'nenhuma')}
        
        IMPORTANTE: Responda APENAS com um JSON válido, sem texto adicional antes ou depois.
        
        {{
            "continua_topico": true,
            "topico_anterior": "descrição_do_topico_anterior",
            "nova_categoria": "politicas_empresa",
            "confianca": 0.8,
            "razao": "explicação_breve"
        }}
        
        As categorias possíveis são: politicas_empresa, procedimentos_ti, problemas_tecnicos, conversa_geral
        """
        
        try:
            response = self.gemini.generate_content(prompt_analise)
            response_text = response.text.strip()
            
            # Tentar extrair JSON da resposta
            # Procurar por { e } para extrair apenas o JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_text = response_text[start_idx:end_idx]
                analise = json.loads(json_text)
                return analise
            else:
                # Se não conseguir extrair JSON, tentar o texto completo
                analise = json.loads(response_text)
                return analise
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao decodificar JSON na análise de continuidade: {e}")
            self.logger.error(f"Resposta recebida: {response.text[:500] if 'response' in locals() else 'N/A'}")
            return {"continua_topico": False, "nova_categoria": "conversa_geral", "confianca": 0.5}
        except Exception as e:
            self.logger.error(f"Erro na análise de continuidade: {e}")
            return {"continua_topico": False, "nova_categoria": "conversa_geral", "confianca": 0.5}
        
    def buscar_conhecimento(self, pergunta: str) -> Optional[str]:
        """Busca na base de conhecimento"""
        pergunta_lower = pergunta.lower()
        
        # Buscar em todas as categorias
        for categoria, items in config.knowledge_base.items():
            for item_key, item_content in items.items():
                # Verificar se alguma palavra-chave está na pergunta
                if any(palavra in pergunta_lower for palavra in item_key.split('_')):
                    return item_content
                    
                # Verificar sinônimos
                if self._verificar_sinonimos(pergunta_lower, item_key):
                    return item_content
        
        return None
    
    def _verificar_sinonimos(self, pergunta: str, item_key: str) -> bool:
        """Verifica sinônimos e variações"""
        sinonimos = {
            'senha': ['password', 'login', 'acesso', 'logon'],
            'wifi': ['internet', 'rede', 'conexão', 'wi-fi'],
            'email': ['e-mail', 'correio', 'mensagem'],
            'impressora': ['printer', 'imprimir'],
            'sistema': ['computador', 'pc', 'máquina']
        }
        
        for palavra_base, lista_sinonimos in sinonimos.items():
            if palavra_base in item_key and any(sin in pergunta for sin in lista_sinonimos):
                return True
        return False
    
    async def conversar(self, mensagem: str, session_id: str = "default") -> Dict:
        """Conversa principal com Gemini usando memória conversacional"""
        try:
            # Analisar continuidade do tópico
            analise_continuidade = self.analisar_continuidade(session_id, mensagem)
            
            # Buscar na base de conhecimento
            conhecimento = self.buscar_conhecimento(mensagem)
            
            # Obter histórico da conversa
            conversa = self.get_or_create_conversation(session_id)
            historico_recente = conversa["historico"][-3:] if conversa["historico"] else []
            
            # Construir contexto baseado na análise
            if analise_continuidade.get("continua_topico", False) and historico_recente:
                # Usuário está continuando o tópico
                newline = "\n"
                contexto_conversa = newline.join([
                    f"Usuário: {h['usuario']}{newline}Bot: {h['bot'][:200]}..." 
                    for h in historico_recente
                ])
                
                prompt = f"""
                Você é Botinho, uma assistente virtual super amigável que lembra das conversas.
                
                CONTEXTO DA CONVERSA ANTERIOR:
                {contexto_conversa}
                
                O usuário está CONTINUANDO o mesmo assunto. Nova mensagem: "{mensagem}"
                
                ANÁLISE: {analise_continuidade.get('razao', '')}
                
                INSTRUÇÕES:
                - Mantenha a continuidade natural da conversa
                - Referencie o que foi discutido antes quando relevante
                - Use frases como "Como estávamos falando...", "Sobre aquilo que você perguntou..."
                - Se encontrou informações específicas na base: {conhecimento if conhecimento else "Sem informações específicas"}
                - Responda de forma contextual e natural
                - Use quebras de linha para organizar a resposta
                """
            else:
                # Novo tópico ou primeira interação
                if conhecimento:
                    prompt = f"""
                    Você é Botinho, uma assistente virtual super amigável.
                    
                    Pergunta do usuário: {mensagem}
                    
                    Informação da base de conhecimento: {conhecimento}
                    
                    {f"CONTEXTO: Anteriormente estávamos falando sobre {analise_continuidade.get('topico_anterior', '')}. Agora o usuário mudou de assunto." if analise_continuidade.get('topico_anterior') else ""}
                    
                    INSTRUÇÕES:
                    - Responda de forma conversacional e natural
                    - Se mudou de assunto, faça uma transição suave
                    - Use expressões humanas como "Ah, posso te ajudar com isso!", "Perfeito!", "Claro!"
                    - Seja empática e acolhedora
                    - Use quebras de linha para organizar melhor a resposta
                    
                    Responda baseado na informação fornecida.
                    """
                else:
                    prompt = f"""
                    Você é Botinho, uma assistente virtual amigável que lembra das conversas.
                    
                    {f"CONTEXTO ANTERIOR: Estávamos falando sobre {analise_continuidade.get('topico_anterior', '')}." if analise_continuidade.get('topico_anterior') else ""}
                    
                    O usuário disse: "{mensagem}"
                    
                    Você não tem informações específicas sobre isso na sua base de conhecimento,
                    mas responda de forma natural e humana, SEMPRE oferecendo as opções disponíveis.
                    
                    INSTRUÇÕES DE FORMATAÇÃO:
                    - Se mudou de assunto, reconheça isso naturalmente
                    - Use quebras de linha para separar seções
                    - Organize as categorias de forma clara
                    - Use emojis para destacar as seções
                    - Mantenha um tom conversacional e amigável
                    
                    IMPORTANTE: Sempre oriente sobre o que você PODE ajudar:
                    
                    🏢 POLÍTICAS DA EMPRESA:
                    • Horário de trabalho e funcionamento  
                    • Política de férias e folgas
                    • Regras de home office
                    • Equipamentos corporativos
                    
                    💻 PROCEDIMENTOS DE TI:
                    • Como resetar senhas
                    • Solicitar novos acessos
                    • Backup e restauração
                    • Configuração de VPN
                    
                    🔧 PROBLEMAS TÉCNICOS:
                    • WiFi não funciona
                    • Email lento ou travado
                    • Problemas com impressoras
                    • Computador ou sistema lento
                    
                    Termine sempre perguntando como pode ajudar especificamente.
                    """
            
            # Gerar resposta com Gemini
            response = self.gemini.generate_content(prompt)
            
            # Processar a resposta para melhor formatação
            resposta_formatada = self._formatar_resposta(response.text)
            
            # Adicionar ao histórico
            categoria = analise_continuidade.get("nova_categoria", "conversa_geral")
            self.adicionar_ao_historico(session_id, mensagem, resposta_formatada, categoria)
            
            return {
                "response": resposta_formatada,
                "confidence": 0.9 if conhecimento else 0.7,
                "context_found": bool(conhecimento),
                "continues_topic": analise_continuidade.get("continua_topico", False),
                "topic_analysis": analise_continuidade,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erro na conversa: {e}")
            return {
                "response": "Opa! Parece que deu uma travadinha aqui do meu lado! 😅<br><br>Pode tentar de novo? Ou se quiser, me conta de uma forma diferente que eu tento entender melhor!",
                "confidence": 0.0,
                "context_found": False,
                "error": True,
                "session_id": session_id
            }
    
    def _formatar_resposta(self, texto: str) -> str:
        """Formata a resposta para melhor exibição na web"""
        # Substituir quebras de linha por <br>
        texto = texto.replace('\n', '<br>')
        
        # Destacar seções com emoji e negrito
        texto = texto.replace('🏢 **POLÍTICAS DA EMPRESA**:', '<br><strong>🏢 POLÍTICAS DA EMPRESA:</strong>')
        texto = texto.replace('💻 **PROCEDIMENTOS DE TI**:', '<br><strong>💻 PROCEDIMENTOS DE TI:</strong>')
        texto = texto.replace('🔧 **PROBLEMAS TÉCNICOS**:', '<br><strong>🔧 PROBLEMAS TÉCNICOS:</strong>')
        
        # Destacar outras formatações em negrito
        import re
        texto = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto)
        
        # Converter listas com • em listas HTML mais elegantes
        linhas = texto.split('<br>')
        texto_final = []
        
        for linha in linhas:
            linha = linha.strip()
            if linha.startswith('•') or linha.startswith('-'):
                # Transformar em item de lista com estilo
                item = linha[1:].strip()
                texto_final.append(f'&nbsp;&nbsp;• {item}')
            else:
                texto_final.append(linha)
        
        resultado = '<br>'.join(texto_final)
        
        # Remover múltiplas quebras consecutivas
        resultado = re.sub(r'(<br>\s*){3,}', '<br><br>', resultado)
        
        return resultado

# Inicializar Botinho
botinho = Botinho()

# FastAPI App
app = FastAPI(
    title="Botinho - Chat AI",
    description="Assistente virtual com Google Gemini Flash 2.0",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat")
async def chat_endpoint(request: Dict):
    message = request.get("message", "")
    session_id = request.get("session_id", f"session_{uuid.uuid4()}")
    
    if not message:
        raise HTTPException(400, "Oops! Parece que você não digitou nada. Digite sua mensagem e eu vou te ajudar! 😊")
    
    try:
        result = await botinho.conversar(message, session_id)
        
        return JSONResponse({
            "response": result["response"],
            "confidence": result["confidence"],
            "context_found": result.get("context_found", False),
            "continues_topic": result.get("continues_topic", False),
            "topic_analysis": result.get("topic_analysis", {}),
            "session_id": result["session_id"],
            "timestamp": result.get("timestamp"),
            "bot_name": "Botinho",
            "model": "Gemini Flash 2.0"
        })
        
    except Exception as e:
        botinho.logger.error(f"Erro no chat: {e}")
        return JSONResponse({
            "response": "Opa! Parece que deu uma travadinha aqui do meu lado! 😅 Pode tentar de novo?",
            "confidence": 0.0,
            "error": True,
            "session_id": session_id
        }, status_code=200)

@app.get("/api/conversation/{session_id}")
async def get_conversation_history(session_id: str):
    """Endpoint para visualizar histórico da conversa (debug)"""
    if session_id in botinho.conversations:
        conversation = botinho.conversations[session_id]
        return JSONResponse({
            "session_id": session_id,
            "created_at": conversation["criado_em"],
            "last_category": conversation.get("ultima_categoria"),
            "history_count": len(conversation["historico"]),
            "history": conversation["historico"]
        })
    else:
        return JSONResponse({"error": "Conversa não encontrada"}, status_code=404)

@app.get("/api/stats")
async def get_stats():
    """Estatísticas das conversas"""
    total_conversations = len(botinho.conversations)
    total_messages = sum(len(conv["historico"]) for conv in botinho.conversations.values())
    
    return JSONResponse({
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "active_sessions": list(botinho.conversations.keys())
    })

@app.get("/", response_class=HTMLResponse)
async def get_main_page():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <title>Botinho - Chat AI</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        
        <!-- Bootstrap Icons -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
        
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            
            .main-content {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 2rem;
            }
            
            .welcome-section {
                text-align: center;
                color: white;
                max-width: 600px;
            }
            
            .welcome-section h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                font-weight: 300;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .welcome-section p {
                font-size: 1.2rem;
                opacity: 0.9;
                line-height: 1.6;
            }
            
            /* CHAT WIDGET FLUTUANTE */
            .chat-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
            }
            
            .chat-toggle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            .chat-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
            }
            
            .chat-toggle .notification-dot {
                position: absolute;
                top: 8px;
                right: 8px;
                width: 12px;
                height: 12px;
                background: #ff4757;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.2); opacity: 0.7; }
                100% { transform: scale(1); opacity: 1; }
            }
            
            .chat-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                display: none;
                flex-direction: column;
                overflow: hidden;
                transform: scale(0.8) translateY(20px);
                opacity: 0;
                transition: all 0.3s ease;
            }
            
            .chat-window.active {
                display: flex;
                transform: scale(1) translateY(0);
                opacity: 1;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .chat-header h3 {
                font-size: 16px;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .close-chat {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                opacity: 0.8;
                transition: opacity 0.2s;
            }
            
            .close-chat:hover {
                opacity: 1;
            }
            
            .chat-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                background: #f8f9fa;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            .chat-messages::-webkit-scrollbar {
                width: 4px;
            }
            
            .chat-messages::-webkit-scrollbar-track {
                background: transparent;
            }
            
            .chat-messages::-webkit-scrollbar-thumb {
                background: #ddd;
                border-radius: 2px;
            }
            
            .message {
                display: flex;
                max-width: 85%;
                word-wrap: break-word;
            }
            
            .message.user {
                align-self: flex-end;
                flex-direction: row-reverse;
            }
            
            .message.bot {
                align-self: flex-start;
            }
            
            .message-content {
                padding: 8px 12px;
                border-radius: 18px;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .message.user .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 4px;
            }
            
            .message.bot .message-content {
                background: white;
                color: #333;
                border: 1px solid #e9ecef;
                border-bottom-left-radius: 4px;
            }
            
            .chat-input {
                padding: 15px;
                border-top: 1px solid #e9ecef;
                background: white;
            }
            
            .input-container {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            
            #messageInput {
                flex: 1;
                border: 1px solid #e9ecef;
                border-radius: 20px;
                padding: 8px 15px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.2s;
            }
            
            #messageInput:focus {
                border-color: #667eea;
            }
            
            #sendButton {
                width: 36px;
                height: 36px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                transition: transform 0.2s;
            }
            
            #sendButton:hover {
                transform: scale(1.1);
            }
            
            #sendButton:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            .typing-indicator {
                display: none;
                align-self: flex-start;
                max-width: 85%;
            }
            
            .typing-content {
                background: white;
                border: 1px solid #e9ecef;
                padding: 8px 12px;
                border-radius: 18px;
                border-bottom-left-radius: 4px;
            }
            
            .typing-dots {
                display: flex;
                gap: 3px;
            }
            
            .typing-dots span {
                width: 6px;
                height: 6px;
                background: #999;
                border-radius: 50%;
                animation: typing 1.4s infinite ease-in-out;
            }
            
            .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
            .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
            .typing-dots span:nth-child(3) { animation-delay: 0s; }
            
            @keyframes typing {
                0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
                40% { transform: scale(1); opacity: 1; }
            }
            
            /* RESPONSIVO */
            @media (max-width: 768px) {
                .chat-window {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 100px);
                    right: 20px;
                    left: 20px;
                    bottom: 80px;
                }
                
                .welcome-section h1 {
                    font-size: 2rem;
                }
                
                .welcome-section p {
                    font-size: 1rem;
                }
            }
        </style>
    </head>
    <body>
        <!-- CONTEÚDO PRINCIPAL -->
        <div class="main-content">
            <div class="welcome-section">
                <h1><i class="bi bi-robot"></i> Botinho</h1>
                <p>Seu assistente virtual inteligente com Google Gemini Flash 2.0. 
                   Clique no ícone no canto inferior direito para iniciar uma conversa!</p>
            </div>
        </div>
        
        <!-- WIDGET DE CHAT FLUTUANTE -->
        <div class="chat-widget">
            <button class="chat-toggle" id="chatToggle">
                <i class="bi bi-chat-dots" id="chatIcon"></i>
                <div class="notification-dot" id="notificationDot"></div>
            </button>
            
            <div class="chat-window" id="chatWindow">
                <div class="chat-header">
                    <h3><i class="bi bi-robot"></i> Botinho</h3>
                    <button class="close-chat" id="closeChat">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <!-- Mensagem inicial será adicionada via JavaScript -->
                </div>
                
                <div class="typing-indicator" id="typingIndicator">
                    <div class="typing-content">
                        <div class="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
                
                <div class="chat-input">
                    <div class="input-container">
                        <input type="text" id="messageInput" 
                               placeholder="Digite sua mensagem..." 
                               onkeypress="handleKeyPress(event)">
                        <button id="sendButton" onclick="sendMessage()">
                            <i class="bi bi-send"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Estado do chat
            let sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            let chatOpen = false;
            let hasNewMessage = false;
            
            // Elementos DOM
            const chatToggle = document.getElementById('chatToggle');
            const chatWindow = document.getElementById('chatWindow');
            const closeChat = document.getElementById('closeChat');
            const chatIcon = document.getElementById('chatIcon');
            const notificationDot = document.getElementById('notificationDot');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            
            // Event listeners
            chatToggle.addEventListener('click', toggleChat);
            closeChat.addEventListener('click', closeChat);
            
            function toggleChat() {
                if (chatOpen) {
                    closeChatWindow();
                } else {
                    openChatWindow();
                }
            }
            
            function openChatWindow() {
                chatWindow.classList.add('active');
                chatIcon.className = 'bi bi-x';
                notificationDot.style.display = 'none';
                chatOpen = true;
                hasNewMessage = false;
                
                // Auto focus no input
                setTimeout(() => {
                    messageInput.focus();
                }, 300);
                
                // Adicionar mensagem inicial se não houver mensagens
                if (document.getElementById('chatMessages').children.length === 0) {
                    addInitialMessage();
                }
            }
            
            function closeChatWindow() {
                chatWindow.classList.remove('active');
                chatIcon.className = 'bi bi-chat-dots';
                chatOpen = false;
            }
            
            function addInitialMessage() {
                const welcomeMessage = `
                    <strong>Oi! 👋 Sou o Botinho!</strong><br><br>
                    Posso te ajudar com:<br>
                    🏢 Políticas da empresa<br>
                    💻 Procedimentos de TI<br>
                    🔧 Problemas técnicos<br><br>
                    Como posso te ajudar hoje?
                `;
                addMessage(welcomeMessage, false);
            }
            
            function addMessage(content, isUser = false) {
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
                
                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                
                if (isUser) {
                    contentDiv.textContent = content;
                } else {
                    contentDiv.innerHTML = content;
                }
                
                messageDiv.appendChild(contentDiv);
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                // Mostrar notificação se chat estiver fechado
                if (!chatOpen && !isUser) {
                    showNotification();
                }
            }
            
            function showNotification() {
                notificationDot.style.display = 'block';
                hasNewMessage = true;
            }
            
            function showTyping() {
                document.getElementById('typingIndicator').style.display = 'flex';
                document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
            }
            
            function hideTyping() {
                document.getElementById('typingIndicator').style.display = 'none';
            }
            
            async function sendMessage() {
                const message = messageInput.value.trim();
                
                if (!message) return;
                
                // Desabilitar envio
                sendButton.disabled = true;
                messageInput.disabled = true;
                
                // Adicionar mensagem do usuário
                addMessage(message, true);
                messageInput.value = '';
                
                // Mostrar indicador de digitação
                showTyping();
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ 
                            message: message,
                            session_id: sessionId
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Erro na requisição');
                    }
                    
                    const data = await response.json();
                    
                    // Esconder indicador de digitação
                    hideTyping();
                    
                    // Adicionar resposta do bot
                    addMessage(data.response);
                    
                } catch (error) {
                    console.error('Erro:', error);
                    hideTyping();
                    addMessage('Ops! Algo deu errado. Tente novamente! 😅');
                } finally {
                    // Reabilitar envio
                    sendButton.disabled = false;
                    messageInput.disabled = false;
                    messageInput.focus();
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                }
            }
            
            // Fechar chat ao clicar fora
            document.addEventListener('click', function(event) {
                if (chatOpen && !chatToggle.contains(event.target) && !chatWindow.contains(event.target)) {
                    closeChatWindow();
                }
            });
            
            // Animação inicial do botão
            setTimeout(() => {
                chatToggle.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    chatToggle.style.transform = 'scale(1)';
                }, 200);
            }, 1000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("🤖 Iniciando Botinho - Chat AI com Gemini Flash 2.0...")
    print("🌐 Interface: http://localhost:8000")
    print("📱 API: http://localhost:8000/api/chat")
    
    uvicorn.run(
        "botinho:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )