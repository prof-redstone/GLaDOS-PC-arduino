import os
import random
import wave
import pyaudio
import threading
import time
import gladosMove
import light
import requests
from pydub import AudioSegment
import io

device_index = 6
isTalking = False

IPTextGeneration = "192.168.1.102"

def getOutputDevice():
    p = pyaudio.PyAudio()
    deviceIndex = 0
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if any(mot in info['name'] for mot in ["T2224zD"]):
            device_index = i
            p.terminate()
            return device_index
    print("La sortie audio T2224zD n'a pas etait trouve, verifier le device de sortie, configuration dans le fichier commande.py")

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
    device_index = getOutputDevice()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=44100,
                    output=True,
                    output_device_index=device_index)

    # Read data and play stream
    gladosMove.talk(1)
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
    gladosMove.talk(0)

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

def process_command(t, mode = "FR"):
    gladosMove.processRecordLed()
    t = t.lower()
    if mode == "FR":
        voiceLineFolder = "E:\\Utilisateurs\\tom\\Bureau\\GLaDOS proj\\voiceLine\\"

        if any(mot in t for mot in ["bonjour", "salut"]):
            play_random_wav(voiceLineFolder + "bonjour")

        if any(mot in t for mot in ["au revoir", "voir"]):
            play_random_wav(voiceLineFolder + "aurevoir")
        
        if any(mot in t for mot in ["ça va"]):
            play_random_wav(voiceLineFolder + "cava")

        if any(mot in t for mot in ["plafond"]) and any(mot in t for mot in ["allume", "allumé"]):
            print("Allumage du plafond")
            light.light_plafond(True)
            play_random_wav(voiceLineFolder + "lumièreOn")

        if any(mot in t for mot in ["bureau"]) and any(mot in t for mot in ["allume", "allumé"]):
            print("Allumage du bureau")
            light.light_bureau(True)
            play_random_wav(voiceLineFolder + "lumièreOn")
        
        if any(mot in t for mot in ["plafond"]) and any(mot in t for mot in ["éteint", "étant", "éteins"]):
            print("Eteint le plafond")
            light.light_plafond(False)
            play_random_wav(voiceLineFolder + "lumièreOff")
            
        if any(mot in t for mot in ["bureau"]) and any(mot in t for mot in ["éteint", "étant", "éteins"]):
            print("Eteint bureau")
            light.light_bureau(False)
            play_random_wav(voiceLineFolder + "lumièreOff")

        if any(mot in t for mot in ["lumière"]) and any(mot in t for mot in ["allume", "allumé"]):
            print("Allumage du plafond et bureau")
            light.light_plafond(True)
            light.light_bureau(True)
            play_random_wav(voiceLineFolder + "lumièreOn")

        if any(mot in t for mot in ["lumière"]) and any(mot in t for mot in ["éteint", "étant", "éteins"]):
            print("Eteint le plafond et bureau")
            light.light_plafond(False)
            light.light_bureau(False)
            play_random_wav(voiceLineFolder + "lumièreOff")
    if mode == "EN":
        import socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IPTextGeneration, 9999))
        
        request = t
        client.send(request.encode('utf-8'))
        
        response = client.recv(1024).decode('utf-8')
        print(f"Réponse reçue : {response}")
        client.close()

        
        url = f'http://{IPTextGeneration}:8124/synthesize/'+response.lower()
        print(url)
        voice = requests.get(url)
        print("get voice ! ")
        if voice.status_code == 200:
            audio_data = io.BytesIO(voice.content)
            audio = AudioSegment.from_wav(audio_data)
            p = pyaudio.PyAudio()
            
            device_index = getOutputDevice()
            stream = p.open(format=pyaudio.paInt16,
                            channels=audio.channels,
                            rate=audio.frame_rate,
                            output=True,
                            output_device_index=device_index)
            audio_bytes = audio.raw_data
            stream.write(audio_bytes)
            stream.stop_stream()
            stream.close()
            p.terminate()
    


if __name__ == "__main__":
    list_audio_devices()
    folder_path = "E:\\Utilisateurs\\tom\\Bureau\\GLaDOS proj\\voiceLine\\bonjour"  
    play_random_wav(folder_path)
