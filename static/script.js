const chatbox = document.getElementById("chatbox");
const toggle = document.getElementById("chat-toggle");
const closeBtn = document.getElementById("chat-close");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const messages = document.getElementById("messages");

toggle.addEventListener("click", () => chatbox.classList.toggle("hidden"));
closeBtn.addEventListener("click", () => chatbox.classList.add("hidden"));

function addMessage(text, type) {
    const el = document.createElement("div");
    el.className = `message ${type}`;
    el.textContent = text;
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";
    sendBtn.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });
        const data = await response.json();
        addMessage(data.reply, "bot");
    } catch (error) {
        addMessage("Sorry, the chatbot could not connect to the Python server.", "bot");
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") sendMessage();
});

document.querySelectorAll(".quick-prompts button").forEach(button => {
    button.addEventListener("click", () => {
        input.value = (button.dataset.q || button.dataset.question || button.textContent);
        sendMessage();
    });
});
