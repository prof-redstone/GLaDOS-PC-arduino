import requests
import time

def send(t):
    try:
        r = requests.get(t, timeout=0.1)
    except :
        pass

if __name__ == "__main__":
    while True:
        send("http://192.168.1.111/api?MainLed=-1")
        send("http://192.168.1.111/api?RingCol=255_100_0")
        send("http://192.168.1.111/api?SecLed=1")
        send("http://192.168.1.111/api?Tilt=0")
        time.sleep(0.5)
        send("http://192.168.1.111/api?Tilt=100")
        time.sleep(0.5)
        send("http://192.168.1.111/api?Tilt=0")
        time.sleep(0.5)
        send("http://192.168.1.111/api?SecLed=2")
        send("http://192.168.1.111/api?Trans=100")
        time.sleep(0.5)
        
        send("http://192.168.1.111/api?Turn=100")
        time.sleep(0.5)
        send("http://192.168.1.111/api?RingCol=255_0_0")
        
        send("http://192.168.1.111/api?Tilt=0")
        time.sleep(0.5)
        send("http://192.168.1.111/api?SecLed=3")
        send("http://192.168.1.111/api?Tilt=100")
        time.sleep(0.5)
        send("http://192.168.1.111/api?Tilt=0")
        time.sleep(0.5)
        send("http://192.168.1.111/api?Trans=0")
        time.sleep(0.5)
        
        send("http://192.168.1.111/api?Turn=0")
        time.sleep(0.5)