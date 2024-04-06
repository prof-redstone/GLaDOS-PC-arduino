import requests
import time

def send(t):
    try:
        r = requests.get(t, timeout=0.2)
    except :
        pass


def turn(x) :
    if (x<=100 and x >=0):
        send(f"http://192.168.1.111/api?Turn={x}")

def tilt(x) :
    if (x<=100 and x >=0):
        send(f"http://192.168.1.111/api?Tilt={x}")

def trans(x) :
    if (x<=100 and x >=0):
        send(f"http://192.168.1.111/api?Trans={x}")

def awake():
    send("http://192.168.1.111/api?SecLed=1")

def record():
    send("http://192.168.1.111/api?SecLed=2")

def processRecord():
    send("http://192.168.1.111/api?SecLed=3")

def talkLed(x):
    if(x == 1 ) :
        send("http://192.168.1.111/api?MainLed=-1")
    if(x == 0 ):
        send("http://192.168.1.111/api?MainLed=0")

def RingCol(x):
    if(x == 0):
        send("http://192.168.1.111/api?RingCol=255_100_0")
    if(x == 1):
        send("http://192.168.1.111/api?RingCol=255_0_0")

def off():
    send("http://192.168.1.111/api?SecLed=0")
    time.sleep(0.1)
    send("http://192.168.1.111/api?RingCol=0_0_0")
    time.sleep(0.1)
    send("http://192.168.1.111/api?MainLed=0")

def on():
    awake()
    time.sleep(0.1)
    RingCol(0)

def esp8266Online():
    try:
        response = requests.get("http://192.168.1.111/ping", timeout=0.5)
        if response.status_code == 200 and response.text.strip() == "pong":
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
    
def talk():
    talkLed(x)


if __name__ == "__main__":
    print(esp8266Online())
    while True:
        off()
        time.sleep(1)
        on()
        talkLed(1)
        RingCol(0)
        awake()
        tilt(0)
        time.sleep(0.5)
        tilt(100)
        time.sleep(0.5)
        tilt(0)
        time.sleep(0.5)
        record()
        trans(100)
        time.sleep(0.5)
        
        turn(100)
        time.sleep(0.5)
        RingCol(1)
        
        tilt(0)
        time.sleep(0.5)
        processRecord()
        tilt(100)
        time.sleep(0.5)
        tilt(0)
        time.sleep(0.5)
        trans(0)
        time.sleep(0.5)
        
        turn(0)
        time.sleep(0.5)