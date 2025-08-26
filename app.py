import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Masukkan webhook Discord-mu
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1409845981578788934/vYf5SNoXHri0WRdC7XxAi4b0Aiy2o6Lq5qS7-BZzAdQxj3R4phdXgQOug3IiFeqs2245"

@app.route("/", methods=["GET"])
def home():
    return "GoBiz Webhook Aktif di Render!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("Data diterima:", data)

        # Ambil field aman
        order_id = data.get("body", {}).get("order", {}).get("order_number", "N/A")
        amount = data.get("body", {}).get("order", {}).get("order_total", 0)
        status = data.get("body", {}).get("order", {}).get("status", "UNKNOWN")

        # Tentukan warna embed: Hijau untuk SUCCESS, Merah untuk FAILED
        color = 0x00FF00 if status.upper() == "SUCCESS" else 0xFF0000

        # Payload embed Discord
        embed = {
            "title": "📦 PEMBAYARAN QRIS",
            "color": color,
            "fields": [
                {"name": "Order ID", "value": str(order_id), "inline": True},
                {"name": "Jumlah", "value": f"Rp{amount:,}", "inline": True},
                {"name": "Status", "value": status, "inline": True}
            ]
        }

        # Kirim ke Discord
        requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]})

        return jsonify({"message": "Webhook diterima"}), 200

    except Exception as e:
        print("Error memproses payload:", e)
        return jsonify({"error": "Invalid payload"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
