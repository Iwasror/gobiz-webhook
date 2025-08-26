import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint tes
@app.route("/", methods=["GET"])
def home():
    return "GoBiz Webhook Aktif di Render!"

# Endpoint webhook dari GoBiz
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Data diterima:", data)

    # Contoh jika status pembayaran berhasil
    if data.get("status") == "SUCCESS":
        print("Pembayaran sukses dari order:", data.get("order_id"))

        # (opsional) kirim notifikasi ke Discord/Telegram
        # import requests
        # requests.post(WEBHOOK_URL, json={"content": f"Pembayaran sukses: {data}"})

    return jsonify({"message": "Webhook diterima"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
