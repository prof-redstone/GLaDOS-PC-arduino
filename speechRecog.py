import os
import gladosMove

def getSpeech():
    from vosk import Model, KaldiRecognizer
    import pyaudio

    model = Model(os.path.dirname(os.path.abspath(__file__))+"\speechRecognition\\vosk-model-small-fr-0.22")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    maxTime = 2 # *5 secondes avant fin
    temps = 0
    gladosMove.recordLed()
    while True:
        if temps >= maxTime:
            return ""

        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            res = text[14:-3]
            if res == "":
                temps+=1
            elif len(res)>1:
                return res
                

if __name__ == "__main__":
    try:
        getSpeech()
    except KeyboardInterrupt:
        pass