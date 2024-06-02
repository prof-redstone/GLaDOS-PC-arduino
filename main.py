import wake_word
import time
import random
import faceRecog
import threading
import gladosMove
import speechRecog
import command
import sys

last_interaction = time.time()
stopProg = False #stop threading function
mode = "FR"

faceRecognition = True
camera4faceRecog = None
if faceRecognition:
    camera4faceRecog = faceRecog.get_camera_index_by_name("Mic-HD Web Ucamera")
faceRecog.point2face(camera4faceRecog)

def MainCoroutine():
    while not stopProg:
        try:
            if wake_word.detect_keyword() == 1:
                on()
                gladosMove.awakeLed()
                face()
                gladosMove.rndMove()
                speech = speechRecog.getSpeech(mode)
                gladosMove.sleepLed()
                face()
                gladosMove.rndMove()
                if speech != "":
                    on()
                    print(speech)
                    command.process_command(speech, mode)
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
        maxTimeON = 30
        while not stopProg:
            if time.time() - last_interaction >= maxTimeON:
                gladosMove.off()
                time.sleep(maxTimeON)
    thread = threading.Thread(target=checkInteractionThread)
    thread.start()

def face():
    if faceRecognition:
        faceRecog.point2face(camera4faceRecog)
    else:
        gladosMove.tilt(random.randint(20, 80))
        gladosMove.turn(random.randint(0, 100))


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            argument = sys.argv[1]
            mode = argument
        print("mode :", mode)
        checkInteraction()
        MainCoroutine()
    except KeyboardInterrupt:
        stopProg = True