# app.py
from backend import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor iniciado en el puerto {port}")
    app.run(debug=True, host="0.0.0.0", port=port)
