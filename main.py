import wake_word
import time
import threading
import gladosMove
import speechRecog


last_interaction = time.time()
stopProg = False #stop threading function

def on():
    global last_interaction
    last_interaction = time.time()
    gladosMove.on()

def checkInteraction():
    def checkInteractionThread():
        maxTimeON = 20
        while not stopProg:
            if time.time() - last_interaction >= maxTimeON:
                gladosMove.off()
                time.sleep(maxTimeON)
    thread = threading.Thread(target=checkInteractionThread)
    thread.start()

def process_command(text):
    gladosMove.processRecordLed()
    if "bonjour" in text:
        print('oui bonjour à toi')
    print(text)

def MainCoroutine():
    while not stopProg:
        if wake_word.detect_keyword() == 1:
            on()
            gladosMove.awakeLed()
            command = speechRecog.getSpeech()
            gladosMove.sleepLed()
            if command != "":
                on()
                process_command(command.lower())
            

if __name__ == "__main__":
    try:
        checkInteraction()
        MainCoroutine()
    except KeyboardInterrupt:
        stopProg = True