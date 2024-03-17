import requests
import time

def send_request(tilt_value, trans_value, led_values):
    tilt_url = f"http://192.168.1.111/api?Tilt={tilt_value}"
    time.sleep(0.2)
    trans_url = f"http://192.168.1.111/api?Trans={trans_value}"
    led_url = f"http://192.168.1.111/api?SecLed={led_values}"
    
    try:
        tilt_response = requests.get(tilt_url)
        print(f"Requêtes envoyées à {tilt_url} et {trans_url}, réponses : Tilt - {tilt_response.status_code}, Trans - {trans_response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête : {e}")

    try:
        time.sleep(0.2)
        trans_response = requests.get(trans_url)
        print(f"Requêtes envoyées à {tilt_url} et {trans_url}, réponses : Tilt - {tilt_response.status_code}, Trans - {trans_response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête : {e}")
    try:
        time.sleep(0.1)
        trans_response = requests.get(led_url)
        print(f"Requêtes envoyées à {tilt_url} et {trans_url}, réponses : Tilt - {tilt_response.status_code}, Trans - {trans_response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête : {e}")


if __name__ == "__main__":
    tilt_values = [0, 100]  # Alternance entre 0 et 100 pour "Tilt"
    trans_values = [0, 100]  # Alternance entre 0 et 100 pour "Trans"
    led_values = [1, 4]  # Alternance entre 0 et 100 pour "Trans"
    index = 0
    
    while True:
        tilt_value = tilt_values[index % len(tilt_values)]
        trans_value = trans_values[index % len(trans_values)]
        led_value = led_values[index % len(led_values)]
        
        send_request(tilt_value, trans_value, led_value)
        
        index += 1
        time.sleep(0.2)