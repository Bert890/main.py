from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        player = data.get("player", "")
        message = data.get("message", "")

        prompt = f"""You are a friendly NPC in a Roblox game.
Player: {message}
Friendly NPC:"""

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7
            }
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        result = response.json()

        print("Hugging Face result:", result)

        if isinstance(result, dict) and "error" in result:
            return jsonify({"reply": "Error from Hugging Face API."})

        reply = result[0]["generated_text"].split("Friendly NPC:")[-1].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Server crashed!", "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
