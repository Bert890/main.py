from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        player = data.get("player", "")
        message = data.get("message", "")

        prompt = f"{player}: {message}\nFriendly NPC:"

        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            HF_MODEL_URL,
            headers=headers,
            json={"inputs": prompt}
        )

        if response.status_code != 200:
            return jsonify({"error": f"Hugging Face API error: {response.text}", "reply": "Server crashed!"}), 500

        output = response.json()
        if isinstance(output, dict) and "error" in output:
            return jsonify({"error": output["error"], "reply": "Model loading or error"}), 503

        generated_text = output[0]["generated_text"].split("Friendly NPC:")[-1].strip()
        return jsonify({"reply": generated_text})

    except Exception as e:
        return jsonify({"error": str(e), "reply": "Server crashed!"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

