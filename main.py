from WakeWord import wake_word
import gladosMove

while True:
    if wake_word.detect_keyword() == 1:
        pass
        #gladosMove.testMove()