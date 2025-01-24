from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)  # Enable logging for debugging


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verify the webhook
        verify_token = os.getenv('VERIFY_TOKEN') # Removed the default value here
        if not verify_token:
            logging.error("VERIFY_TOKEN environment variable not set!")
            return "Verification failed: missing verification token", 500

        if request.args.get('hub.verify_token') == verify_token:
            challenge = request.args.get('hub.challenge')
            if challenge:
               return challenge, 200 # Verification success: Respond with the challenge
            else:
               logging.error("Verification failed: No challenge provided")
               return "Verification failed: missing challenge", 400 

        logging.error("Verification failed: Token mismatch")
        return "Verification failed: token mismatch", 403

    elif request.method == 'POST':
        # Handle incoming messages
        try:
            data = request.get_json() # Use get_json to handle json parsing errors
            logging.info("Received data: %s", data)  # Log the incoming data with logging

             #Process WhatsApp message here
           # Example:
           #  if data and 'entry' in data and data['entry']:
           #      for entry in data['entry']:
           #           if 'changes' in entry and entry['changes']:
           #              for change in entry['changes']:
           #                  if 'value' in change and 'messages' in change['value'] and change['value']['messages']:
           #                       for message in change['value']['messages']:
           #                            logging.info("Message Recieved : %s", message)

            return "OK", 200

        except Exception as e:
             logging.error("Error processing POST data: %s", str(e))
             return jsonify({'error': 'Invalid JSON'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)