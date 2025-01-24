from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Environment variables for WhatsApp API
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'your_verify_token')  # Webhook verification token
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')  # WhatsApp API access token
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')  # WhatsApp Business phone number ID

# Root endpoint
@app.route('/')
def home():
    return "Welcome to the WhatsApp Chatbot!"

# Webhook endpoint for WhatsApp
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verify the webhook
        hub_verify_token = request.args.get('hub.verify_token')
        if hub_verify_token == VERIFY_TOKEN:
            return request.args.get('hub.challenge')  # Return challenge for verification
        return "Verification failed: Invalid token", 403

    elif request.method == 'POST':
        # Handle incoming messages
        data = request.json
        print("Incoming data:", data)  # Log incoming data for debugging

        try:
            # Extract message and sender ID from the incoming payload
            message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            sender_id = data['entry'][0]['changes'][0]['value']['messages'][0]['from']

            # Log the received message and sender ID
            print(f"Received message from {sender_id}: {message}")

            # Send a reply back to the user
            send_message(sender_id, f"You said: {message}")
            return "OK", 200

        except KeyError as e:
            print(f"Error processing incoming message: {e}")
            return "Invalid message format", 400

# Function to send a message via WhatsApp API
def send_message(recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "text": {"body": message}
    }

    # Send the message using the WhatsApp API
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Message sent to {recipient_id}: {message}")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.json()}")

# Run the Flask app
if __name__ == '__main__':
    # Use the port provided by the environment or default to 5000 for local testing
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)