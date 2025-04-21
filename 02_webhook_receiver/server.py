from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        # Process the received data here
        print(f"Received webhook data: {data}")
        if data.get('event') == 'renter_session.approved':
            with open("approved_session.json", "a") as f:
                json.dump(data, f, indent=2)
        return jsonify({"status": "success", "message": "Webhook received"}), 200
    return jsonify({"status": "error", "message": "Invalid request method"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)