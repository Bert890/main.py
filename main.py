from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    player = data.get("player", "")
    message = data.get("message", "")

    prompt = f"""You are a very friendly NPC in a Roblox game.
Player: {message}
Friendly NPC:"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.95,
            "repetition_penalty": 1.1
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    if isinstance(result, dict) and "error" in result:
        return jsonify({"reply": "Sorry, I'm having trouble right now."})

    reply = result[0]["generated_text"].split("Friendly NPC:")[-1].strip()
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


