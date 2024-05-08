import os
import random
import wave
import pyaudio
import threading
import time
import gladosMove
import light

device_index = 6
isTalking = False

def play_random_wav(folder_path):
    global isTalking
    wav_files = [file for file in os.listdir(folder_path) if file.endswith('.wav')]
    if not wav_files:
        print("Aucun fichier .wav trouvé dans le dossier spécifié.")
        return

    random_wav = random.choice(wav_files)
    file_path = os.path.join(folder_path, random_wav)

    wf = wave.open(file_path, 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=44100,
                    output=True,
                    output_device_index=device_index)

    # Read data and play stream
    data = wf.readframes(1024)
    while data:
        if not isTalking :
            isTalking = True
            talk()
        stream.write(data)
        data = wf.readframes(1024)
    isTalking = False
    stream.stop_stream()
    stream.close()
    p.terminate()

def list_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']}, {info['hostApi']}, {info['maxInputChannels']} input channels, {info['maxOutputChannels']} output channels")
    p.terminate()


def talk():
    gladosMove.sleepLed()
    def talkThread():
        global isTalking
        while isTalking:
            gladosMove.rndMove()
            time.sleep(1)
    thread = threading.Thread(target=talkThread)
    thread.start()

def process_command(t):
    gladosMove.processRecordLed()
    t = t.lower()

    if any(mot in t for mot in ["bonjour", "salut"]):
        play_random_wav("E:\\Utilisateurs\\tom\\Bureau\\GLaDOS proj\\voiceLine\\bonjour")

    if any(mot in t for mot in ["au revoir", "voir"]):
        play_random_wav("E:\\Utilisateurs\\tom\\Bureau\\GLaDOS proj\\voiceLine\\aurevoir")
    
    if any(mot in t for mot in ["ça va"]):
        play_random_wav("E:\\Utilisateurs\\tom\\Bureau\\GLaDOS proj\\voiceLine\\cava")

    if any(mot in t for mot in ["plafond"]) and any(mot in t for mot in ["allume", "allumé"]):
        print("Allumage du plafond")
        light.light_plafond(True)

    if any(mot in t for mot in ["bureau"]) and any(mot in t for mot in ["allume", "allumé"]):
        print("Allumage du bureau")
        light.light_bureau(True)
    
    if any(mot in t for mot in ["plafond"]) and any(mot in t for mot in ["éteint", "étant", "éteins"]):
        print("Eteint le plafond")
        light.light_plafond(False)
        
    if any(mot in t for mot in ["bureau"]) and any(mot in t for mot in ["éteint", "étant", "éteins"]):
        print("Eteint bureau")
        light.light_bureau(False)

    if any(mot in t for mot in ["lumière"]) and any(mot in t for mot in ["allume", "allumé"]):
        print("Allumage du plafond et bureau")
        light.light_plafond(True)
        light.light_bureau(True)

    if any(mot in t for mot in ["lumière"]) and any(mot in t for mot in ["éteint", "étant", "éteins"]):
        print("Eteint le plafond et bureau")
        light.light_plafond(False)
        light.light_bureau(False)
    


if __name__ == "__main__":
    #list_audio_devices()
    folder_path = "E:\\Utilisateurs\\tom\\Bureau\\GLaDOS proj\\voiceLine\\bonjour"  
    play_random_wav(folder_path)
