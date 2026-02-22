const state = {
  sessionId: `session_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`,
};

const messagesContainer = document.getElementById("messages");
const form              = document.getElementById("chatForm");
const input             = document.getElementById("messageInput");
const sendButton        = document.getElementById("sendButton");

function formatTime() {
  return new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
}

/**
 * Append a chat message and return the wrapper element.
 * @param {string} text
 * @param {"bot"|"user"} sender
 */
function appendMessage(text, sender) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.textContent = text;

  const time = document.createElement("span");
  time.className = "message-time";
  time.textContent = formatTime();

  wrapper.appendChild(bubble);
  wrapper.appendChild(time);
  messagesContainer.appendChild(wrapper);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  return wrapper;
}

/** Show an animated typing indicator while waiting for the API response. */
function showTyping() {
  const wrapper = document.createElement("div");
  wrapper.className = "message bot typing";
  wrapper.id = "typingIndicator";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    dot.className = "typing-dot";
    bubble.appendChild(dot);
  }

  wrapper.appendChild(bubble);
  messagesContainer.appendChild(wrapper);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/** Remove the typing indicator. */
function hideTyping() {
  document.getElementById("typingIndicator")?.remove();
}

/* ── Initial greeting ─────────────────────────────────────────────────────── */
appendMessage(
  "Olá. Sou o Botinho. Posso ajudar com políticas da empresa, procedimentos de TI e problemas técnicos.",
  "bot",
);

/* ── Submit handler ───────────────────────────────────────────────────────── */
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  input.value = "";
  sendButton.disabled = true;
  showTyping();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: state.sessionId }),
    });

    const data = await response.json();
    hideTyping();

    if (!response.ok) {
      const fallback = data?.error?.message ?? "Erro ao processar solicitação.";
      appendMessage(fallback, "bot");
      return;
    }

    appendMessage(data.response, "bot");
  } catch {
    hideTyping();
    appendMessage("Falha de conexão com a API. Tente novamente.", "bot");
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
});
