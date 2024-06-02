import gladosMove
import time
import win32com.client


deviceName = "Mic-HD Web Ucamera"

def list_video_devices():
    devices = []
    objSWbemServices = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objSWbemServices.ConnectServer(".", "root\\cimv2")
    colItems = objSWbemServices.ExecQuery("Select Name from Win32_PnPEntity")
    
    device_names = [objItem.Name for objItem in colItems]
    
    for name in device_names:
        if name and ("camera" in name.lower() or "video" in name.lower()):
            devices.append(name)
    
    return devices

def get_camera_index_by_name(name):
    devices = list_video_devices()
    for idx, device_name in enumerate(devices):
        if name in device_name:
            return idx
    print("camera not found")
    return None

def analyze_frame(camera_index, show_window=False):
    import cv2
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f"Erreur : Impossible d'ouvrir la caméra {camera_index}")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Erreur : Impossible de lire l'image de la caméra")
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    results = []
    for (x, y, w, h) in faces:
        results.append((x, y, w, h))
        print(f"Face detected at: X={x}, Y={y}, Width={w}, Height={h}")

    if show_window:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Face Detection', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return results

def fastFace(camera_index):
    import cv2
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f"Erreur : Impossible d'ouvrir la caméra {camera_index}")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Erreur : Impossible de lire l'image de la caméra")
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    frame_height, frame_width = gray.shape[:2]

    nX = -1
    nY = -1
    for (x, y, w, h) in faces:
        nX = x / frame_width
        nY = y / frame_height
        break
    #print(nX, nY)

    return (nX, nY)


def main():
    devices = list_video_devices()
    print("Available video devices:")
    for idx, name in enumerate(devices):
        print(f"{idx}: {name}")

    camera_name = input("Enter the camera name to select: ")
    camera_index = get_camera_index_by_name(camera_name)
    
    if camera_index is None:
        print(f"Camera named '{camera_name}' not found.")
        return

    print(f"Using camera index: {camera_index}")

    show_window = False  # afficher la fenêtre
    analyze_frame(camera_index, show_window)


def face(deviceInd):
    global deviceName
    if deviceInd == None:
        deviceInd = get_camera_index_by_name(deviceName)
    if deviceInd is None:
        print(f"Camera named '{deviceName}' not found.")
        return
    return fastFace(deviceInd)


def point2face(deviceInd = None):
    print("reco face")
    (x,y) = face(deviceInd)
    mapX = [0.33, 0.03]
    mapY = [0.23, 0.80]
    ny = (y-mapY[0])/(mapY[1]-mapY[0]) * 100
    nx = (x-mapX[0])/(mapX[1]-mapX[0]) * 100
    if x == -1 or y == -1:
        return
        ny = 50
        nx = 50
    nx = min(100, max(0, nx))
    ny = min(100, max(0, ny))
    #print(nx, ny)
    gladosMove.turn(nx)
    time.sleep(0.1)
    gladosMove.tilt(ny)
    time.sleep(0.1)

if __name__ == "__main__":
    while True:
        point2face()
