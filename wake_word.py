import os
import pvporcupine
import struct
import pyaudio

def listMic():
    global pa
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        # print(device_info['name'])

def detect_keyword():
    print("\nListening for GLaDOS keyword ...")
    
    ACCESS_KEY = ""
    KEYWORD_FILE_PATH = ""
    MIC_INDEX = None
    
    # Charge la clé d'accès et le fichier de mot-clé
    with open(os.path.dirname(os.path.abspath(__file__)) + "\WakeWord\Porcupine\KEY.key", 'r') as fichier:
        ACCESS_KEY = fichier.readline().strip()
    
    KEYWORD_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\WakeWord\\Porcupine\\glad-os_en_windows_v3_0_0.ppn"
    
    # Lit le nom du microphone configuré
    try:
        with open("configInputDevice.txt", "r") as f:
            nom_device_config = f.read().strip()
    except FileNotFoundError:
        print("Le fichier configInputDevice.txt est introuvable. Veuillez exécuter configInputDevice.py pour configurer le microphone.")
        return None
    
    # Recherche du périphérique d'entrée correspondant
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if info['name'] == nom_device_config:
            MIC_INDEX = i
            break
    
    if MIC_INDEX is None:
        print(f"Le microphone '{nom_device_config}' n'a pas été trouvé. Veuillez vérifier le périphérique d'entrée ou exécuter configInputDevice.py pour le configurer.")
        pa.terminate()
        return None
    
    print("Mic input index for wake word :", MIC_INDEX)
    
    # Initialise Porcupine pour la détection du mot-clé
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_FILE_PATH]
    )

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length,
                    input_device_index=MIC_INDEX)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Wake-Word Detected")
            porcupine.delete()
            return 1

if __name__ == "__main__":
    try:
        listMic()
    except KeyboardInterrupt:
        pass