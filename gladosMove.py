import requests
import time
import threading

valTilt = 50
valTrans = 50
valTurn = 50

def send(t):
    def send_req():
        try:
            r = requests.get(t, timeout=0.1)
        except :
            pass
    thread = threading.Thread(target=send_req)
    thread.start()


def turn(x) :
    if (x<=100 and x >=0):
        send(f"http://192.168.1.111/api?Turn={x}")

def tilt(x) :
    if (x<=100 and x >=0):
        send(f"http://192.168.1.111/api?Tilt={x}")

def trans(x) :
    if (x<=100 and x >=0):
        send(f"http://192.168.1.111/api?Trans={x}")

def awakeLed():
    send("http://192.168.1.111/api?SecLed=1")

def recordLed():
    send("http://192.168.1.111/api?SecLed=2")

def processRecordLed():
    send("http://192.168.1.111/api?SecLed=3")

def talkLed():
    send("http://192.168.1.111/api?SecLed=4")

def talk(x):
    if(x == 1 ) :
        send("http://192.168.1.111/api?MainLed=-1")
    if(x == 0 ):
        send("http://192.168.1.111/api?MainLed=0")

def RingCol(r,g,b):
    send(f"http://192.168.1.111/api?RingCol={r}_{g}_{b}")

def off():
    send("http://192.168.1.111/api?SecLed=0")
    time.sleep(0.1)
    send("http://192.168.1.111/api?RingCol=0_0_0")
    time.sleep(0.1)
    send("http://192.168.1.111/api?MainLed=0")

def on():
    RingCol(120,110,90)
    time.sleep(0.2)
    awakeLed()
    time.sleep(0.2)
    RingCol(255,100,0)

def esp8266Online():
    try:
        response = requests.get("http://192.168.1.111/ping", timeout=0.5)
        if response.status_code == 200 and response.text.strip() == "pong":
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

def testMove():
    while True:
        off()
        time.sleep(1)
        on()
        talk(1)
        RingCol(255,100,0)
        awakeLed()
        tilt(0)
        time.sleep(0.5)
        tilt(100)
        time.sleep(0.5)
        tilt(0)
        time.sleep(0.5)
        recordLed()
        trans(100)
        time.sleep(0.5)
        
        turn(100)
        time.sleep(0.5)
        RingCol(255,0,0)
        
        tilt(0)
        time.sleep(0.5)
        processRecordLed()
        tilt(100)
        time.sleep(0.5)
        tilt(0)
        time.sleep(0.5)
        trans(0)
        time.sleep(0.5)
        
        turn(0)
        time.sleep(0.5)


if __name__ == "__main__":
    testMove()
