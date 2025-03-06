document.getElementById("sendButton").addEventListener("click", sendMessage);

async function sendMessage() {
    let userInput = document.getElementById("userInput").value.trim();
    if (!userInput) return;

    // Append user message to chat UI
    appendMessage("You", userInput);

    // Send message to Flask backend
    try {
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput }),
        });

        let data = await response.json();
        if (data.response) {
            appendMessage("Amor", data.response);
        }
    } catch (error) {
        console.error("Error:", error);
        appendMessage("Amor", "Oops! Something went wrong. Try again later.");
    }

    // Clear input field
    document.getElementById("userInput").value = "";
}

function appendMessage(sender, message) {
    let chatBox = document.getElementById("chatBox");
    let messageElement = document.createElement("div");
    messageElement.classList.add("p-3", "rounded-lg", "my-2", sender === "You" ? "bg-blue-200" : "bg-pink-200");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);

    // Auto-scroll to latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}
