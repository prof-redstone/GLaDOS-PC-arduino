import wake_word
import time
import threading
import gladosMove
import speechRecogFR
import command


last_interaction = time.time()
stopProg = False #stop threading function


def MainCoroutine():
    while not stopProg:
        try:
            if wake_word.detect_keyword() == 1:
                on()
                gladosMove.awakeLed()
                gladosMove.rndMove()
                speech = speechRecogFR.getSpeech()
                gladosMove.sleepLed()
                gladosMove.rndMove()
                if speech != "":
                    on()
                    print(speech)
                    command.process_command(speech)
        except Exception as error:
            print(error)
            #command.play_random_wav("E:\\Utilisateurs\\tom\\Bureau\\GLaDOS proj\\voiceLine\\problème" )
            gladosMove.off()  

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


if __name__ == "__main__":
    try:
        checkInteraction()
        MainCoroutine()
    except KeyboardInterrupt:
        stopProg = True