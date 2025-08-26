import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1409845981578788934/vYf5SNoXHri0WRdC7XxAi4b0Aiy2o6Lq5qS7-BZzAdQxj3R4phdXgQOug3IiFeqs2245"

# Endpoint tes
@app.route("/", methods=["GET"])
def home():
    return "GoBiz Webhook Aktif di Render!"

# Endpoint webhook dari GoBiz
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Data diterima:", data)

    # contoh notifikasi
    message = f"📢 Webhook diterima:\n```{data}```"

    # kirim ke Discord
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": message})
    except Exception as e:
        print("Gagal kirim ke Discord:", e)

    return jsonify({"message": "Webhook diterima"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
