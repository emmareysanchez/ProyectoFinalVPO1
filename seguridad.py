from picamera2 import PiCamera2
from time import sleep
import numpy as np
import cv2
import matplotlib.pyplot as plt
# VERIFICAR EN QUE ESPACIO DE COLOR ESTAN LAS IMAGENES


# carga de imagenes y las convierte a RGB
# img_rojo = cv2.imread('ImagenesSeguridad/rojo.jpg')
# img_rojo = cv2.cvtColor(img_rojo, cv2.COLOR_BGR2RGB)

# img_azul = cv2.imread('ImagenesSeguridad/azul.jpg')
# img_azul = cv2.cvtColor(img_azul, cv2.COLOR_BGR2RGB)

# img_verde = cv2.imread('ImagenesSeguridad/verde.jpeg')
# img_verde = cv2.cvtColor(img_verde, cv2.COLOR_BGR2RGB)

# img_amarillo = cv2.imread('ImagenesSeguridad/amarillo.jpg')
# img_amarillo = cv2.cvtColor(img_amarillo, cv2.COLOR_BGR2RGB)


# filtro azul
def filtrado_azul(img):
    limite_inferior = np.array([100, 100, 100] )
    limite_superior = np.array([140, 255, 255])
    imagen_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    filtro = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
    parecido = sum(sum(filtro // 255))
    return parecido


# filtro rojo
def filtrado_rojo(img):
    limite_inferior = np.array([0, 50, 50] )
    limite_superior = np.array([20, 255, 255])
    imagen_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    filtro = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
    parecido = sum(sum(filtro // 255))
    return parecido


# filtro amarillo
def filtrado_amarillo(img):
    limite_inferior = np.array([0, 100, 100] )
    limite_superior = np.array([50, 255, 255])
    imagen_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    filtro = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
    parecido = sum(sum(filtro // 255))
    return parecido


# filtro verde
def filtrado_verde(img):
    limite_inferior = np.array([20, 50, 50] )
    limite_superior = np.array([80, 255, 255])
    imagen_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    filtro = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
    parecido = sum(sum(filtro // 255))
    return parecido


def establecer_color(imagen):
    verde = 1
    azul = 2
    amarillo = 3
    rojo = 4

    filtro_verde = filtrado_verde(imagen)
    fitro_azul = filtrado_azul(imagen)
    filtro_rojo = filtrado_rojo(imagen)
    filtro_amarillo = filtrado_amarillo(imagen)

    if fitro_azul > filtro_rojo and fitro_azul > filtro_amarillo and fitro_azul > filtro_verde:
        return azul
    elif filtro_rojo > fitro_azul and filtro_rojo > filtro_amarillo and filtro_rojo > filtro_verde:
        return rojo
    elif filtro_amarillo > fitro_azul and filtro_amarillo > filtro_rojo and filtro_amarillo > filtro_verde:
        return amarillo
    elif filtro_verde > fitro_azul and filtro_verde > filtro_rojo and filtro_verde > filtro_amarillo:
        return verde
    else:
        return 0


def verificar_combinacion(imagenes) -> bool:
    # combinacion: azul, amarillo, rojo, rojo, verde, azul
    # verde = 1, azul = 2, amarillo = 3, rojo = 4
    combinacion = [2, 3, 4, 4, 1, 2]
    lista_colores = list()
    for i in range(len(imagenes)):
        img = imagenes[i]
        lista_colores.append(establecer_color(img))
    if lista_colores == combinacion:
        verificacion = True
    else:
        verificacion = False
    return verificacion


def load_calibration_params(file_path):
    try:
        calibration_data = np.load(file_path)
        camera_matrix = calibration_data['camera_matrix']
        dist_coeffs = calibration_data['dist_coeffs']
        return camera_matrix, dist_coeffs
    except Exception as e:
        print(f"Error loading calibration parameters: {e}")
        return None, None


def undistort_image(image, camera_matrix, dist_coeffs):
    h, w = image.shape[:2]
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_image

# VERIFICAR EN QUE ESPACIO DE COLOR ESTAN LAS IMAGENES
def introducir_codigo(calibration_file):
    # Conectamos la camara y la configuramos
    picam = Picamera2()
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    imagenes = list()
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
            imagenes.append(undistorted_frame)
            if len(imagenes) == 6:
                combinacion_correcta = verificar_combinacion(imagenes)
                imagenes = list()
        if combinacion_correcta:
            break

