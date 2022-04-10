import logging
import os
from twilio.rest import Client

from flask import Flask
from flask_ask import Ask, request, session, question, statement

import RPi.GPIO as GPIO
import time
import requests
import json

# Raspberry Pi Pins Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

# Initialize Flask Ask
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# Twilio Credentials
account_sid = os.environ['SID']
auth_token = os.environ['TOKEN']
client = Client(account_sid, auth_token)

GPIO.output(23, GPIO.LOW)

# Twilio Message Function
def twilMsg(channel): 
   print("Received input, sending message now.")
   message = client.messages \
    .create(
         body='$DOGE is trading at {}.'.format(doge_price),
         from_='+19124612542',
         to='+917827794110'
     )
    print(message.sid)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(23, GPIO.LOW)

@ask.launch
def launch():
    speech_text = 'Welcome to Coin Watch.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('PriceIntent')
def Price_Intent():
    if int(doge_price) < 0.14368:
        return statement('Doge Coin is trading below purchase price at', doge_price)

    elif int(doge_price) > 0.14368:
        return statement('Doge coin is trading above purchase price at', doge_price)
        
    else:
        return statement('Sorry, data could not be processed.')

@ask.intent('StatusIntent')
def Status_Intent():
    speech_text = 'The hardware is working.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask me about the price of Doge Coin and I will tell you if it is trading above your purchase or not.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('AMAZON.StopIntent')
def stop():
    speech_text = 'Goodbye!'
    return statement(speech_text).simple_card(speech_text)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    speech_text = 'Goodbye!'
    return statement(speech_text).simple_card(speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)

response_API = requests.get('https://sochain.com//api/v2/get_price/DOGE/USD')
print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)
doge_price = parse_json['data']['prices'][0]['price']
print("Doge is trading at ", doge_price)

GPIO.add_event_detect(18, GPIO.FALLING, callback = twilMsg, bouncetime = 2000)

while 1:  
   time.sleep(1)