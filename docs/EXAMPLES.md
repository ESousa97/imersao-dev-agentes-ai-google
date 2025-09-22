# 💡 Exemplos de Uso - Botinho

## Índice
- [Exemplos Básicos](#exemplos-básicos)
- [Conversas com Memória](#conversas-com-memória)
- [Base de Conhecimento](#base-de-conhecimento)
- [API Examples](#api-examples)
- [Casos de Uso Práticos](#casos-de-uso-práticos)
- [Personalização](#personalização)

## Exemplos Básicos

### 1. Primeira Conversa
```
Usuário: Olá!
Botinho: Olá! 👋 Sou o Botinho, sua assistente virtual inteligente! 
         Posso ajudar com políticas da empresa, procedimentos de TI 
         e resolver problemas técnicos. Em que posso ajudá-lo hoje?

Usuário: Como você funciona?
Botinho: Funciono com tecnologia Google Gemini Flash 2.0 e tenho um 
         sistema de memória que me permite lembrar de nossas conversas! 
         📚 Tenho conhecimento sobre políticas empresariais, procedimentos 
         de TI e soluções para problemas técnicos. Posso ajudar de forma 
         contextualizada e personalizada!
```

### 2. Pergunta Simples
```
Usuário: Qual o horário de trabalho?
Botinho: 🕐 **Horário de Trabalho**
         
         Horário de trabalho: 8h às 18h, segunda a sexta-feira
         
         Precisa de mais alguma informação sobre políticas da empresa?
```

## Conversas com Memória

### 3. Contexto Mantido
```
# Primeira mensagem
Usuário: Como resetar minha senha?
Botinho: 🔑 **Reset de Senha**
         
         Para resetar sua senha, siga estes passos:
         1. Acesse o portal → 'Esqueci senha' 
         2. Verificar email
         
         Você conseguiu acessar o portal?

# Segunda mensagem (mantém contexto)
Usuário: E se eu não receber o email?
Botinho: Continuando sobre o reset de senha... 📧
         
         Se não recebeu o email de recuperação:
         • Verifique a caixa de spam/lixo eletrônico
         • Confirme se o email cadastrado está correto
         • Aguarde até 10 minutos (pode haver delay)
         • Se persistir, entre em contato com o suporte de TI
         
         O email ainda não chegou?

# Terceira mensagem (contexto expandido)
Usuário: Preciso falar com o TI então
Botinho: Perfeito! Para questões de senha que não conseguimos resolver 
         pelo portal, o TI é mesmo a melhor opção. 🛠️
         
         **Como contactar o TI:**
         • Abra um ticket no sistema interno
         • Mencione que tentou o reset pelo portal
         • Informe que não recebeu o email de recuperação
         
         Quer que eu explique como abrir um ticket?
```

### 4. Mudança de Tópico Detectada
```
# Conversa sobre senha
Usuário: Como resetar minha senha?
Botinho: [Resposta sobre senha...]

# Mudança para outro assunto
Usuário: A impressora não está funcionando
Botinho: Vejo que mudamos de assunto - agora vamos resolver o problema 
         da impressora! 🖨️
         
         **Problemas com Impressora:**
         1. Verificar papel (se há papel suficiente)
         2. Verificar tinta (níveis dos cartuchos)
         3. Reiniciar equipamento
         4. Verificar se está conectada à rede
         
         Qual desses itens você já verificou?
```

## Base de Conhecimento

### 5. Políticas da Empresa
```
Usuário: Posso trabalhar de casa?
Botinho: 🏠 **Política de Home Office**
         
         Home office: até 2 dias por semana com aprovação do gestor
         
         📋 **Como solicitar:**
         • Fale com seu gestor direto
         • Defina quais dias da semana
         • Garanta que tem estrutura adequada em casa
         
         Já conversou com seu gestor sobre isso?

Usuário: E sobre férias?
Botinho: 🏖️ **Política de Férias**
         
         Política de férias: solicitar com 30 dias de antecedência 
         via sistema
         
         📅 **Dicas importantes:**
         • Planeje com antecedência
         • Use o sistema oficial da empresa
         • Confirme aprovação antes de fazer planos
         
         Está planejando férias para quando?
```

### 6. Procedimentos de TI
```
Usuário: Preciso de acesso ao sistema financeiro
Botinho: 💼 **Solicitação de Acessos**
         
         Para solicitar acessos a sistemas:
         • Abra um ticket no sistema interno
         • Especifique qual sistema precisa acessar
         • Justifique a necessidade do acesso
         • Informe seu gestor para aprovação
         
         **Sistema Financeiro** geralmente requer aprovação especial. 
         Seu gestor já está ciente dessa necessidade?

Usuário: Como abrir um ticket?
Botinho: Vou te ajudar com o processo de abertura de ticket! 🎫
         
         **Passo a passo:**
         1. Acesse o portal interno da empresa
         2. Vá na seção "Suporte" ou "TI"
         3. Clique em "Novo Ticket"
         4. Preencha:
            - Categoria: "Solicitação de Acesso"
            - Sistema: "Sistema Financeiro"
            - Justificativa: [sua necessidade]
            - Gestor: [nome do seu gestor]
         
         Precisa de ajuda com algum campo específico?
```

### 7. Problemas Técnicos
```
Usuário: Meu computador está muito lento
Botinho: 🐌 **Sistema Lento - Vamos resolver!**
         
         Soluções rápidas:
         1. ✅ Fechar programas desnecessários
         2. ✅ Reiniciar o PC
         3. ✅ Verificar espaço em disco
         4. ✅ Limpar arquivos temporários
         
         Vamos começar: quantos programas você tem abertos agora?

Usuário: Uns 15 programas
Botinho: Aí está o problema! 😅 15 programas são muitos e podem deixar 
         o sistema lento.
         
         **Ação imediata:**
         • Feche programas que não está usando
         • Mantenha apenas os essenciais
         • Use Ctrl+Shift+Esc para ver uso de memória
         
         **Dica:** Computadores corporativos funcionam melhor com 5-7 
         programas simultâneos no máximo.
         
         Após fechar alguns programas, o desempenho melhorou?
```

## API Examples

### 8. Requisição via cURL
```bash
# Primeira mensagem
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "mensagem": "Olá, preciso de ajuda com backup",
       "session_id": "user123"
     }'

# Resposta
{
  "resposta": "Olá! Vou ajudar você com backup! 💾...",
  "session_id": "user123",
  "timestamp": "2025-09-22T20:15:30",
  "categoria": "procedimentos_ti",
  "usou_conhecimento": true,
  "analise_continuidade": {
    "continua_topico": false,
    "nova_categoria": "procedimentos_ti",
    "confianca": 0.9
  }
}
```

### 9. JavaScript/Fetch
```javascript
// Função para enviar mensagem
async function enviarMensagem(mensagem, sessionId = null) {
    try {
        const response = await fetch('http://localhost:8000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mensagem: mensagem,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro:', error);
        return null;
    }
}

// Exemplo de uso
const resposta = await enviarMensagem("Como fazer backup?", "sessao-123");
console.log(resposta.resposta);
```

### 10. Python Client
```python
import requests
import json

class BotinhoClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    def chat(self, mensagem):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "mensagem": mensagem,
                "session_id": self.session_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.session_id = data.get("session_id")
            return data
        else:
            return {"erro": response.text}

# Uso
client = BotinhoClient()

# Primeira pergunta
resposta1 = client.chat("Qual a política de férias?")
print(resposta1["resposta"])

# Segunda pergunta (mantém contexto)
resposta2 = client.chat("E quanto tempo posso tirar?")
print(resposta2["resposta"])
```

## Casos de Uso Práticos

### 11. Onboarding de Funcionário
```
Usuário: Sou novo na empresa, o que preciso saber?
Botinho: Bem-vindo à empresa! 🎉 É ótimo ter você no time!
         
         **Informações Essenciais para Novos Funcionários:**
         
         🕐 **Horário:** 8h às 18h, segunda a sexta
         🏠 **Home Office:** Até 2 dias/semana (com aprovação)
         🔑 **Acessos:** Solicite via ticket no sistema interno
         💾 **Backup:** Automático às 2h (restore sob demanda)
         🌐 **VPN:** Obrigatória para acesso remoto
         
         Sobre o que gostaria de saber mais detalhes?

Usuário: Como solicitar acessos aos sistemas?
Botinho: Perfeito! Vou te guiar no processo de solicitação de acessos 🎯
         
         **Passo a passo detalhado:**
         1. Acesse o portal interno da empresa
         2. Seção "Suporte" → "Novo Ticket"
         3. Categoria: "Solicitação de Acesso"
         4. Informe: sistema específico + justificativa
         5. Mencione seu gestor para aprovação
         
         **Dica de novo funcionário:** Fale primeiro com seu gestor 
         sobre quais sistemas você precisará. Isso acelera o processo!
         
         Já sabe quais sistemas vai precisar?
```

### 12. Suporte Técnico Escalado
```
Usuário: A internet caiu aqui no escritório
Botinho: 🌐 **Problema de Conectividade - Vamos resolver!**
         
         **Verificações básicas:**
         1. ✅ Reiniciar roteador (desconectar 30seg)
         2. ✅ Verificar cabos de rede
         3. ✅ Testar em outros dispositivos
         
         Se for problema geral do escritório:
         🆘 **Contactar TI imediatamente**
         
         É só no seu computador ou outros também estão sem internet?

Usuário: É geral, todo mundo está sem internet
Botinho: Entendi! É um problema de infraestrutura. 🚨
         
         **Ação necessária:**
         • Abra um ticket URGENTE para o TI
         • Categoria: "Infraestrutura - Rede"
         • Prioridade: ALTA
         • Mencione que afeta todo o escritório
         
         **Enquanto aguarda:**
         • Use conexão móvel se necessário
         • Comunique a equipe sobre o problema
         • Documente horário do início da falha
         
         Quer que eu te oriente a abrir o ticket urgente?
```

### 13. Gerenciamento de Expectativas
```
Usuário: Preciso de uma resposta sobre licença médica urgente
Botinho: Entendo a urgência da sua situação! 🏥
         
         **Sobre licenças médicas:**
         Este é um assunto específico que requer atenção do RH, 
         pois envolve questões legais e documentação específica.
         
         **Ação recomendada:**
         📞 Contate o RH diretamente
         📧 Email: rh@empresa.com
         ☎️ Ramal: 1234
         
         **Documentos geralmente necessários:**
         • Atestado médico original
         • Formulário de licença preenchido
         
         ⚠️ **Importante:** Para questões urgentes de saúde, o RH 
         tem procedimentos específicos que não posso orientar 
         completamente.
         
         Conseguiu contatar o RH?
```

## Personalização

### 14. Adicionando Nova Categoria
```python
# No arquivo botinho.py, adicionar à knowledge_base:
"recursos_humanos": {
    "licenca_medica": "Para licença médica: apresentar atestado no RH em até 48h",
    "vale_refeicao": "Vale refeição: R$ 25/dia, crédito automático toda segunda",
    "plano_saude": "Plano de saúde: coparticipação de R$ 50 por consulta",
    "beneficios": "Benefícios: VR, VT, plano de saúde, seguro de vida"
}
```

**Resultado:**
```
Usuário: Quanto é o vale refeição?
Botinho: 🍽️ **Vale Refeição**
         
         Vale refeição: R$ 25/dia, crédito automático toda segunda
         
         O valor é creditado automaticamente na sua conta todo início 
         de semana. Alguma dúvida sobre como usar?
```

### 15. Sinônimos Personalizados
```python
# Expandir dicionário de sinônimos
sinonimos = {
    'senha': ['password', 'login', 'acesso', 'logon', 'credencial'],
    'wifi': ['internet', 'rede', 'conexão', 'wi-fi', 'wireless'],
    'vale_refeicao': ['vr', 'vale-refeição', 'alimentação', 'comida'],
    'plano_saude': ['plano médico', 'convênio', 'saúde', 'médico']
}
```

### 16. Respostas Contextuais Avançadas
```python
# Exemplo de resposta que considera histórico
def resposta_contextual(self, categoria_anterior, nova_categoria):
    if categoria_anterior == "problemas_tecnicos" and nova_categoria == "procedimentos_ti":
        return "Vejo que saímos de problemas técnicos para procedimentos. Posso ajudar com o processo administrativo agora! 📋"
    elif categoria_anterior == "politicas_empresa" and nova_categoria == "problemas_tecnicos":
        return "Mudando de políticas para questões técnicas. Vamos resolver esse problema! 🔧"
    else:
        return ""
```

---

**💡 Dica:** Todos esses exemplos podem ser testados na interface web em `http://localhost:8000` ou via API conforme demonstrado!