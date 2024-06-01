import os
import gladosMove
import pyaudio

def getInputDevice():
    mic = pyaudio.PyAudio()
    for i in range(mic.get_device_count()):
        device_info = mic.get_device_info_by_index(i)
        #print(device_info['name'])
        if("Microphone (Mic-HD Web Ucamera)" == device_info['name']):
            mic.terminate()
            return i

def getSpeech(mode = "FR"):
    from vosk import Model, KaldiRecognizer

    if mode == "FR":
        model = Model(os.path.dirname(os.path.abspath(__file__))+"\speechRecognition\\vosk-model-small-fr-0.22") 
    if mode == "EN":
        model = Model(os.path.dirname(os.path.abspath(__file__))+"\speechRecognition\\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    
    MIC_INDEX = getInputDevice()
    print("device index for input :", MIC_INDEX)
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192, input_device_index=MIC_INDEX)
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
        mic = pyaudio.PyAudio()
        MIC_INDEX = 0
        for i in range(mic.get_device_count()):
            device_info = mic.get_device_info_by_index(i)
            #print(device_info['name'])
        while True:
            print(getSpeech())
    except KeyboardInterrupt:
        pass