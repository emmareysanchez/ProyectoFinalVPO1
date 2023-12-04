from picamera2 import Picamera2
from time import sleep
import numpy as np
import cv2
import matplotlib.pyplot as plt


# filtro azul
def filtrado_azul(img):
    limite_inferior = np.array([100, 100, 100] )
    limite_superior = np.array([140, 255, 255])
    imagen_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filtro = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
    parecido = sum(sum(filtro // 255))
    return parecido


# filtro rojo
def filtrado_rojo(img):
    limite_inferior = np.array([0, 50, 50] )
    limite_superior = np.array([20, 255, 255])
    imagen_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filtro = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
    parecido = sum(sum(filtro // 255))
    return parecido


# filtro verde
def filtrado_verde(img):
    limite_inferior = np.array([20, 50, 50] )
    limite_superior = np.array([80, 255, 255])
    imagen_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filtro = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
    parecido = sum(sum(filtro // 255))
    return parecido


def establecer_color(imagen):
    verde = 1
    azul = 2
    # amarillo = 3
    rojo = 3
    filtro_verde = filtrado_verde(imagen)
    fitro_azul = filtrado_azul(imagen)
    filtro_rojo = filtrado_rojo(imagen)
    # filtro_amarillo = filtrado_amarillo(imagen)

    if fitro_azul > filtro_rojo and fitro_azul > filtro_verde:
        return azul
    elif filtro_rojo > fitro_azul and filtro_rojo > filtro_verde:
        return rojo
    elif filtro_verde > fitro_azul and filtro_verde > filtro_rojo:
        return verde
    else:
        return 0


def verificar_combinacion(imagenes) -> bool:
    # combinacion: azul, rojo, rojo, verde, azul
    # verde = 1, azul = 2, rojo = 3
    combinacion = [2, 3, 3, 1, 2]
    lista_colores = list()
    for i in range(len(imagenes)):
        img = imagenes[i]
        lista_colores.append(establecer_color(img))
    if lista_colores == combinacion:
        verificacion = True
        mensaje = 'Combinacion correcta'
    else:
        verificacion = False
        mensaje = 'Combinacion Incorrecta'
    print(mensaje)
    return verificacion


def load_calibration_params(file_path):
    try:
        calibration_data = np.load(file_path)
        camera_matrix = calibration_data['mtx']
        dist_coeffs = calibration_data['dist']
        return camera_matrix, dist_coeffs
    except Exception as e:
        print(f"Error loading calibration parameters: {e}")
        return None, None


def undistort_image(image, camera_matrix, dist_coeffs):
    h, w = image.shape[:2]
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_image

def introducir_codigo(calibration_file):
    # Conectamos la camara y la configuramos
    picam = Picamera2()
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    imagenes = list()
    combinacion_correcta = False
    # Cargar parámetros de calibración
    camera_matrix, dist_coeffs = load_calibration_params(calibration_file)
    while True:
        frame = picam.capture_array()
        # Corregimos la distorsión
        undistorted_frame = undistort_image(frame, camera_matrix, dist_coeffs)
        cv2.imshow("picam", undistorted_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            # Mandar imagen
            print(establecer_color(undistorted_frame))
            imagenes.append(undistorted_frame)
            if len(imagenes) == 5:
                combinacion_correcta = verificar_combinacion(imagenes)
                imagenes = list()
        if combinacion_correcta:
            break
    picam.close()

