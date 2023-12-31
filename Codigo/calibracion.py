import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt


def calibracion():
    print('Iniciando calibración...\n')
    circle_board_size = (5, 4) # Tamaño del tablero circular
    circle_size_mm = 50

    # Crear objeto para almacenar las coordenadas 3D del tablero circular
    objp = np.zeros((circle_board_size[0] * circle_board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:circle_board_size[0], 0:circle_board_size[1]].T.reshape(-1, 2) * circle_size_mm

    # Listas para almacenar coordenadas 3D e 2D del tablero
    obj_points = []  # Coordenadas 3D del mundo real
    img_points = []  # Coordenadas 2D en la imagen

    # Obtener la lista de nombres de archivos de imágenes en la carpeta
    image_folder = 'ImagenesCalibracion/'  # Reemplaza con la ruta de tu carpeta
    image_files = glob.glob(f'{image_folder}*.jpg')  # Puedes ajustar la extensión de archivo según tus imágenes
    for image in image_files:
        # Leer la imagen
        img = cv2.imread(image)
        imagen_circulos = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Intentar encontrar el patrón de círculos en la imagen
        ret, corners = cv2.findCirclesGrid(gray, circle_board_size, flags=cv2.CALIB_CB_SYMMETRIC_GRID)
        for i in corners:
            cv2.circle(imagen_circulos, tuple(map(int, i[0])), 2, (0, 255, 0), -1)

        if ret:
            obj_points.append(objp)
            img_points.append(corners)

    # Calibrar la cámara
    rms, mtx, dist, _, _ = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    print("Matriz de intrínsecos:\n", mtx)
    print("Coeficientes de distorsión:\n", dist)
    print("root mean square reprojection error:\n", rms)

    nombre = 'parametros_calibracion.npz'

    # Guardar los parámetros de calibración en un archivo
    np.savez(nombre, mtx=mtx, dist=dist)

    print(f'Calibración completada. Parámetros guardados en {nombre}.\n')
    return nombre
