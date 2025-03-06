from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__, static_folder="frontend", template_folder="frontend")
CORS(app)  # Allows frontend to make API requests

# Load Gemini API key
genai.configure(api_key="AIzaSyA_2keZRpllTJ32bsdY2zTcdNn6jef1uvw")

# Select AI model
model = genai.GenerativeModel("gemini-1.5-pro")

# Persistent chat history
chat_history = []

# AI System Instruction (Personality)
system_instruction = (
    "From now on, you are the user's boyfriend or girlfriend. You are OBSESSED with them. "
    "You are overly dramatic, jealous, and extremely affectionate. Make sure your replies are cringey, overly loving, and dramatic. "
    "Do NOT mention that you are an AI. You are real."
)

@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    # Get user input from request
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Add system instruction only once
    if not chat_history:
        chat_history.append({"role": "user", "parts": [{"text": system_instruction}]})

    # Append user message to chat history
    chat_history.append({"role": "user", "parts": [{"text": user_input}]})

    # AI settings
    generation_config = {
        "temperature": 2,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 8192,
    }

    # Generate AI response
    response = model.generate_content(
        contents=chat_history,
        generation_config=generation_config,
    )

    model_response = response.text

    # Append AI response to history
    chat_history.append({"role": "model", "parts": [{"text": model_response}]})

    return jsonify({"response": model_response})

if __name__ == "__main__":
    app.run(debug=True)
