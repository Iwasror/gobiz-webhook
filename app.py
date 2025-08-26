import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1409845981578788934/vYf5SNoXHri0WRdC7XxAi4b0Aiy2o6Lq5qS7-BZzAdQxj3R4phdXgQOug3IiFeqs2245"

@app.route("/", methods=["GET"])
def home():
    return "GoBiz Webhook Aktif di Render!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Ambil JSON dari request
        data = request.get_json(force=True)
        print("Data diterima:", data)

        # Ambil field aman pakai get()
        order_id = data.get("body", {}).get("order", {}).get("order_number", "N/A")
        amount = data.get("body", {}).get("order", {}).get("order_total", 0)
        status = data.get("body", {}).get("order", {}).get("status", "UNKNOWN")

        # Buat notifikasi Discord
        msg = (
            f"✅ **PEMBAYARAN** ✅\n"
            f"📦 Order ID : {order_id}\n"
            f"💰 Jumlah   : Rp{amount:,}\n"
            f"📌 Status   : {status}"
        )

        # Kirim ke Discord
        try:
            requests.post(DISCORD_WEBHOOK, json={"content": msg})
        except Exception as e:
            print("Gagal kirim ke Discord:", e)

        return jsonify({"message": "Webhook diterima"}), 200

    except Exception as e:
        print("Error memproses payload:", e)
        return jsonify({"error": "Invalid payload"}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
