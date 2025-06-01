import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "")
        print(f"📨 Mensaje recibido: {user_input}")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://tupagina.com",  # Opcional
            "X-Title": "ChatBot Monografía"         # Opcional
        }

        payload = {
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code != 200:
            print("❌ Error:", response.status_code, response.text)
            return jsonify({"error": response.text}), response.status_code

        result = response.json()
        bot_response = result["choices"][0]["message"]["content"]

        return jsonify({"response": bot_response})

    except Exception as e:
        print("❌ Error en /chat:", e)
        return jsonify({"error": str(e)}), 500
