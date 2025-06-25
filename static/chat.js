// chat.js - Handles chatbot UI and communication

let selectedCareer = window.careerName || "";
let chatContainer = document.getElementById("chat-container");
let messagesDiv = document.getElementById("chat-messages");
let inputField = document.getElementById("user-input");
let typingIndicator;

function toggleChat() {
  chatContainer.style.display =
    chatContainer.style.display === "flex" ? "none" : "flex";
  document.getElementById("chatbot-launcher").style.display = "block";
}

function sendMessage() {
  const msg = inputField.value.trim();
  if (!msg) return;

  addMessage("You", msg, "#f0f0f0");
  inputField.value = "";

  showTyping();

  fetch("/chatbot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg, career: selectedCareer }),
  })
    .then((res) => res.json())
    .then((data) => {
      hideTyping();
      addMessage("Bot", formatBotReply(data.reply), "#f4e6fa");
    })
    .catch((err) => {
      hideTyping();
      addMessage("Bot", "Sorry, something went wrong.", "#f4e6fa");
    });
}

function showTyping() {
  typingIndicator = document.createElement("div");
  typingIndicator.classList.add("message", "bot-message");
  typingIndicator.innerHTML = `<em>Bot is typing...</em>`;
  messagesDiv.appendChild(typingIndicator);
  scrollToBottom();
}

function hideTyping() {
  if (typingIndicator) {
    typingIndicator.remove();
    typingIndicator = null;
  }
}

function addMessage(sender, text, color) {
  const messageEl = document.createElement("div");
  messageEl.classList.add("message");
  messageEl.style.backgroundColor = color;
  messageEl.innerHTML = `<strong>${sender}:</strong> ${text}`;
  messagesDiv.appendChild(messageEl);
  scrollToBottom();
}

function scrollToBottom() {
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function formatBotReply(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br>");
}

inputField.addEventListener("keydown", function (e) {
  if (e.key === "Enter") sendMessage();
});

// Show floating hint with animation and dismiss option
setTimeout(() => {
  const hint = document.createElement("div");
  hint.id = "chat-float-hint";
  hint.innerHTML = `
    <span>💡 Want to know more about the predicted career?</span>
    <span id="close-hint" style="margin-left: 10px; cursor: pointer;">❌</span>
  `;
  document.body.appendChild(hint);

  document.getElementById("close-hint").onclick = () => {
    hint.style.opacity = "0";
    hint.style.transform = "translateY(20px)";
    setTimeout(() => hint.remove(), 300);
  };
}, 3000);
