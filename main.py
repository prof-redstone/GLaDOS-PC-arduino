from WakeWord import wake_word
import gladosMove

if wake_word.detect_keyword() == 1:
    gladosMove.testMove()