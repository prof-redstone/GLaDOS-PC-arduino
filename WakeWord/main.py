import sys 
import threading
import speech_recognition
import pyttsx3 as tts

from neuralintents import GenericAssistant

class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        self.assistant = GenericAssistant("intents.json")
        self.assistant.train_model()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google_cloud(audio)
                    text = text.lower()

                    print(text)
            except:
                continue


Assistant()