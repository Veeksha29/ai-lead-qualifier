// ---------- CONFIG ----------
const API_URL = "http://127.0.0.1:8001/chat";

// ---------- DOM ----------
const chat = document.getElementById("chat");
const input = document.getElementById("input");

// ---------- HELPERS ----------
function addMessage(text, cls) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function addSuggestions(suggestions) {
  const div = document.createElement("div");
  div.className = "suggestions";

  suggestions.forEach(option => {
    const btn = document.createElement("button");
    btn.innerText = option;
    btn.onclick = () => sendMessage(option);
    div.appendChild(btn);
  });

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// ---------- CORE ----------
async function sendMessage(text = null) {
  const message = text || input.value.trim();
  if (!message) return;

  // Show user message
  addMessage(message, "user");
  input.value = "";

  console.log("📤 Sending to backend:", message);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error("HTTP error " + response.status);
    }

    const data = await response.json();
    console.log("📥 Backend response:", data);

    // Handle response types
    if (data.type === "question") {
      addMessage(data.question, "bot");
      addSuggestions(data.suggestions || []);
    } 
    else if (data.type === "lead_ready") {
      addMessage("✅ Lead Ready!", "bot");
      addMessage(JSON.stringify(data.data, null, 2), "bot");
    } 
    else if (data.type === "clarification") {
      addMessage(data.question, "bot");
      addSuggestions(data.suggestions || []);
    } 
    else {
      addMessage("🤔 Something unexpected happened.", "bot");
    }

  } catch (error) {
    console.error("❌ Frontend error:", error);
    addMessage("⚠️ Error talking to server. Check backend.", "bot");
  }
}

// ---------- ENTER KEY SUPPORT ----------
input.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

// ---------- RESET ----------
async function resetChat() {
  chat.innerHTML = "";
  input.value = "";

  try {
    await fetch("http://127.0.0.1:8001/reset", {
      method: "POST"
    });
  } catch (err) {
    console.error("Backend reset failed", err);
  }

  addMessage(
    "👋 New conversation started. Tell me what you are looking for.",
    "bot"
  );
}


// ---------- CONFIRM JS LOADED ----------
console.log("✅ app.js loaded successfully");
