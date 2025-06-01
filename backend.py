# backend.py
from app import app
from flask import request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("🔐 OPENROUTER_API_KEY cargada:", os.getenv("OPENROUTER_API_KEY") is not None)

# Inicializar cliente OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        return f"Template error: {e}", 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        user_input = data.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        print(f"📨 Mensaje recibido: {user_input}")

        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1000,
            temperature=0.7
        )

        bot_response = response.choices[0].message.content
        print("✅ Respuesta del modelo:", bot_response)
        
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"❌ Error en /chat: {str(e)}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
