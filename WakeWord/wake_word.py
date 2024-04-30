import os
import pvporcupine
import struct
import pyaudio


def detect_keyword():
    print("\nListening for GLaDOS keyword ...")
        
    ACCESS_KEY = ""
    KEYWORD_FILE_PATH = ""
    MIC_INDEX = 0

    with open(os.path.dirname(os.path.abspath(__file__)) + "\Porcupine\KEY.key", 'r') as fichier:
        ACCESS_KEY = fichier.readline().strip()

    with open(os.path.dirname(os.path.abspath(__file__)) + "\Porcupine\KEY.key", 'r') as fichier:
        KEYWORD_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\Porcupine\\glad-os_en_windows_v3_0_0.ppn"


    global pa
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        if("Microphone (USB Audio)" == device_info['name']):
            MIC_INDEX = i
            break
    porcupine = None
    audio_stream = None
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
        detect_keyword()
    except KeyboardInterrupt:
        pass