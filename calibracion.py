import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import time

# Tamaño del tablero circular (filas, columnas)
circle_board_size = (4, 5)
circle_size_mm = 50
circle_distance_centre_cm = 5

# Crear objeto para almacenar las coordenadas 3D del tablero circular
objp = np.zeros((circle_board_size[0] * circle_board_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:circle_board_size[0], 0:circle_board_size[1]].T.reshape(-1, 2) * circle_size_mm

# Listas para almacenar coordenadas 3D e 2D del tablero
obj_points = []  # Coordenadas 3D del mundo real
img_points = []  # Coordenadas 2D en la imagen

# Obtener la lista de nombres de archivos de imágenes en la carpeta
image_folder = 'ImagenesCalibracion'  # Reemplaza con la ruta de tu carpeta
image_files = glob.glob(f'{image_folder}/*.jpg')  # Puedes ajustar la extensión de archivo según tus imágenes

for image in image_files:
    # Leer la imagen
    img = cv2.imread(image)
    imagen_circulos = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Intentar encontrar el patrón de círculos en la imagen
    ret, corners = cv2.findCirclesGrid(gray, circle_board_size, flags=cv2.CALIB_CB_SYMMETRIC_GRID)
    print(ret, corners)
    for i in corners:
        print(1, i[0], type(i[0][0]), type(i[0][1]))
        cv2.circle(imagen_circulos, tuple(map(int, i[0])), 2, (0, 255, 0), -1)
    plt.imshow(imagen_circulos)
    plt.show()
    time.sleep(1)



    if ret:
        obj_points.append(objp)
        img_points.append(corners)

# Calibrar la cámara
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Guardar los parámetros de calibración en un archivo
np.savez('calibration_params.npz', mtx=mtx, dist=dist)

print('Calibración completada. Parámetros guardados en calibration_params.npz')