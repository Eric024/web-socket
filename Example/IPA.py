import websocket
from threading import Thread
import requests
import json
from pprint import pprint
#from matrix_lite import led
#import RPi.GPIO as GPIO
import datetime
import time

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(3, GPIO.OUT)

def say(text):
    url = "http://localhost:12101/api/text-to-speech"
    requests.post(url, text)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        say("Good Morning!")
    elif hour>=12 and hour<18:
        say("Good Afternoon!")
    else:
        say("Good Evening!")
    say("Welcome! Please tell me how may I help you")

# Intents are passed through here
def on_message(ws, message):
    data = json.loads(message)
    print("\n**Captured New Intent**\n")
    print("\n<<< Intent file >>>\n")
    print("\n__________________________________________________________________________________\n")
    print(json.dumps(data,indent = 1))
    print("\n__________________________________________________________________________________\n")

    if ("TellTime" == data["intent"]["name"]):
        #GPIO.output(3, True)
        #time.sleep(3)
        #GPIO.output(3, False)
        #led.set(data["slots"]["color"])
        #say("Device changed to: " + data["slots"]["color"])
        say("Device changed to red light")
    elif ("Meeting" == data["intent"]["name"]):
        say("Yes, We have one meeting today")

def on_error(ws, error):
    print("\nError from Intent >>>\n",error)

def on_close(ws):
    print("\n**Disconnected**\n")

def on_open(ws):
    print("\n**Connected**\n")

# Wake Word

def on_Message(wake,message):
    print("\n**Wake word detected**\n")
    print("\n<<< Message from Porcupine >>>\n")
    print("\n__________________________________________________________________________________\n")
    pprint(message)
    print("\n__________________________________________________________________________________\n")

def on_Error(wake, err):
    print("\nError from Porcupine >>>\n",err)

def on_Close(wake):
    print("\n**Wake word Disconnected**\n")

def on_Open(wake):
    print("\n**Wake word Connected**\n")

# Start web socket client
if __name__ == "__main__":
    wishMe()
    ws = websocket.WebSocketApp("ws://localhost:12101/api/events/intent",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              on_open = on_open)
    wake = websocket.WebSocketApp("ws://localhost:12101/api/events/wake",
                              on_message = on_Message,
                              on_error = on_Error,
                              on_close = on_Close,
                              on_open = on_Open)
    t1 = Thread(target = ws.run_forever)
    t2 = Thread(target = wake.run_forever)
    # starting threads 
    t1.start()
    t2.start()
  
    # wait until all threads finish 
    t1.join()
    t2.join()
    print ("Exiting Main Thread")
