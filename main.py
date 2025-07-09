from flask import Flask, request, jsonify
import openai
import os

print("Using OpenAI version:", openai.__version__)

app = Flask(__name__)
openai.api_key = os.environ['OPENAI_API_KEY']

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    player = data.get("player", "")

    prompt = f"""You are a very friendly NPC in a Roblox game. Be cheerful and helpful when responding to the player.

Player: {message}
Friendly NPC:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.8
    )

    npc_reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": npc_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway gives you this
    app.run(host="0.0.0.0", port=port)

