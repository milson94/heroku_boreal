from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

# Webhook endpoint
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verify the webhook
        verify_token = os.getenv('VERIFY_TOKEN', 'your_verify_token')
        if request.args.get('hub.verify_token') == verify_token:
            return request.args.get('hub.challenge')
        return "Verification failed", 403

    elif request.method == 'POST':
        # Handle incoming messages
        data = request.json
        print(data)  # Log the incoming data
        return "OK", 200

        # Extract message and sender ID
        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            sender_id = data['entry'][0]['changes'][0]['value']['messages'][0]['from']

            # Send a reply
            send_message(sender_id, f"You said: {message}")
        except KeyError:
            print("Invalid message format")

        return "OK", 200

def send_message(recipient_id, message):
    # Get environment variables
    access_token = os.getenv('ACCESS_TOKEN')  # Your WhatsApp API access token
    phone_number_id = os.getenv('PHONE_NUMBER_ID')  # Your WhatsApp Business phone number ID

    # Send message using WhatsApp API
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "text": {"body": message}
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Message sent:", response.status_code, response.json())

if __name__ == '__main__':
    # Use the port provided by Heroku or default to 5000 for local testing
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)