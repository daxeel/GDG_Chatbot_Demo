# Author : Daxeel Soni
# Email  : daxeelsoni44@gmail.com
# Web    : http://daxeel.github.io
# About  : Dictionary based Telegram chatbot python server file

#Import modules
import time
import telepot
import requests
import json

# Telegram bot token
TOKEN = '359911433:AAEnwh2pR4Y3TGI3qXK0UFlS0YC1m8K1Kfo'

def handle(msg):
	
	# Message details
	content_type, chat_type, chat_id = telepot.glance(msg) # ('text', u'private', 238366033)

	# Process text messages
	if content_type == 'text':
		bot.sendChatAction(chat_id, "typing")
		user_message = msg['text']

		# Calling dictionary API
		res = json.loads(requests.get("https://api.import.io/store/connector/debc3d00-bab7-408a-9c3f-339beff62703/_query?input=webpage%2Furl%3Ahttps%3A%2F%2Fglosbe.com%2Fen%2Fen%2F" + user_message + "&&_apikey=5b5fd39b293d467a96a3ae991b8af88bf05390ea32dede72c808e95892bd1eff9549aed258aa36b1c0beca77e7d58f9efd66f8680ba152e7f7599f1e7056cd8f211ae67c876c4107da3a9e19a7b396ff").text)
		definition = res['results'][0]['description']

		# Send message back to user
		bot.sendMessage(chat_id, definition)

# Init telegram bot
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
	time.sleep(10)
