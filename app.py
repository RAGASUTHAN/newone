import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

import chatbot_config

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from the .env file.")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        response = client.models.generate_content(
            model=chatbot_config.MODEL_NAME,
            contents=message,
            config={
                "system_instruction": chatbot_config.SYSTEM_INSTRUCTION,
                "temperature": 0.7,
                "max_output_tokens": 1024,
            },
        )

        answer = response.text or "Sorry, I could not generate a response."
        return jsonify({"response": answer})

    except Exception as error:
        return jsonify({
            "error": "Sorry, the assistant could not respond right now.",
            "details": str(error),
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
