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
        
        # Verificar que la API key existe
        if not api_key:
            print("❌ Error: OPENROUTER_API_KEY no encontrada")
            return jsonify({"error": "API key no configurada"}), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:5000",  # Cambiado a localhost para desarrollo
            "X-Title": "ChatBot Monografía"
        }

        payload = {
            "model": "mistralai/devstral-small:free",
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        print(f"🔑 API Key recibida:", repr(api_key))
        print(f"📤 Enviando payload: {payload}")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers, 
            json=payload,
            timeout=30  # Añadir timeout
        )

        print(f"📥 Status code: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")

        if response.status_code != 200:
            print("❌ Error:", response.status_code, response.text)
            return jsonify({
                "error": f"API Error: {response.status_code}",
                "details": response.text
            }), response.status_code

        result = response.json()
        print(f"📥 Response JSON: {result}")
        
        # Verificar que la respuesta tiene la estructura esperada
        if "choices" not in result or len(result["choices"]) == 0:
            print("❌ Error: Respuesta inesperada de la API")
            return jsonify({"error": "Respuesta inesperada de la API"}), 500
            
        bot_response = result["choices"][0]["message"]["content"]
        return jsonify({"response": bot_response})

    except requests.exceptions.RequestException as e:
        print("❌ Error de conexión:", e)
        return jsonify({"error": "Error de conexión con la API"}), 500
    except Exception as e:
        print("❌ Error en /chat:", e)
        return jsonify({"error": str(e)}), 500