# Import python modules
import os
import sys
import json
import requests
from flask import Flask, request

# Initialize flask server
app = Flask(__name__)

# Facebook credentials
PAGE_ACCESS_TOKEN = "PAGE_TOKEN"
VERIFY_TOKEN = "VERIFY_TOKEN"

# Chatbot verification from facebook app
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Working!", 200

# Process incoming messages
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    
                    # Calling dictionary API
                    res = json.loads(requests.get("https://api.import.io/store/connector/debc3d00-bab7-408a-9c3f-339beff62703/_query?input=webpage%2Furl%3Ahttps%3A%2F%2Fglosbe.com%2Fen%2Fen%2Fcomputer&&_apikey=5b5fd39b293d467a96a3ae991b8af88bf05390ea32dede72c808e95892bd1eff9549aed258aa36b1c0beca77e7d58f9efd66f8680ba152e7f7599f1e7056cd8f211ae67c876c4107da3a9e19a7b396ff").text)
                    definition = res['results'][0]['description']

                    if len(definition) > 0:
                        send_message(sender_id, "Searching...")
                        send_message(sender_id, definition)
                    else:
                        send_message(sender_id, "Not found.")

    return "ok", 200

# Method to send text messages
def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

# Run flask server
if __name__ == '__main__':
    app.run(debug=True)
