import cv2
from picamera2 import Picamera2

def stream_video():
    picam = Picamera2()
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    n_imagen = 1
    while True:
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('h'):
            cv2.imwrite(f'Imagen_mermelada{n_imagen}.jpg', frame)
            n_imagen += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()
