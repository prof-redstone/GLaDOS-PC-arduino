# configInputDevice.py
import pyaudio

def choisir_microphone():
    p = pyaudio.PyAudio()
    devices = []
    
    # Liste les périphériques d'entrée audio (microphones)
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:  # Filtre pour ne garder que les entrées audio
            devices.append((i, info['name']))
            print(f"{i}: {info['name']}")
    
    # Demande à l'utilisateur de choisir un microphone
    choix = int(input("Entrez le numéro du microphone à utiliser : "))
    
    # Vérifie que le choix est valide
    if any(choix == device[0] for device in devices):
        nom_device = next(name for index, name in devices if index == choix)
        
        # Enregistre le nom du périphérique dans le fichier de config
        with open("configInputDevice.txt", "w") as f:
            f.write(nom_device)
        
        print(f"Le microphone '{nom_device}' a été enregistré dans configInputDevice.txt.")
    else:
        print("Numéro de périphérique invalide. Réessayez.")
    
    p.terminate()

if __name__ == "__main__":
    choisir_microphone()
