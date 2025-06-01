from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    print("📩 Mensaje recibido:", user_input)  # 👈 log para depurar

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.5-pro-exp-03-25",
            messages=[
                {"role": "system", "content": "Eres un asistente amigable."},
                {"role": "user", "content": user_input}
            ]
        )
        print("✅ Respuesta OpenRouter:", response)
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        print("❌ Error al llamar a OpenRouter:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
print("🔐 OPENROUTER_API_KEY cargada:", os.getenv("OPENROUTER_API_KEY") is not None)