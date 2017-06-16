# Import python modules
import os
import sys
import json
import requests
from flask import Flask, request

# Initialize flask server
app = Flask(__name__)

# Facebook credentials
PAGE_ACCESS_TOKEN = "EAAVNSagZBUMIBAMb89moYytPBZBBU8ZAZBHT34wJY9CyMUB9XedF5RihfeXmSmgZB5PDEKmWpErUTikCHKfaJcbAZBwa8ALKgPVG2tuiDvp4x0X4MkOgO4gnZC4TmfKPmAGBnKMgcPuMeXs1vgsq9yhzZAqpDcs1THZB8yHMZACUc82AZDZD"
VERIFY_TOKEN = "gdg_bot_token"

# Chatbot verification from facebook app
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

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
                  
                    link= requests.get("http://memes-kashyapb.rhcloud.com/"+str(message_text)).text
                    image_link=json.loads(link)
                    image_link=image_link['data'][0]['link']
                    if message_text in ["hi", "hello", "hola"]:
                        send_message(sender_id, "Hello form GDG Meetup!")
                       
                    else:
                         send_image(sender_id, image_link)
                    

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

# Method to send images
def send_image(recipient_id, img_url):
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
            "attachment": {
                "type":"image",
                "payload": {
                    "url": img_url
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


# Run flask server
if __name__ == '__main__':
    app.run(debug=True)
