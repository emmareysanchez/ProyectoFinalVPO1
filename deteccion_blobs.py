import cv2
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import blob_log, blob_dog
from skimage.color import rgb2gray
from threading import Thread
import time


def encontrar_blobs(imagen):
    imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detectar blobs utilizando LoG (Laplacian of Gaussian)
    blobs_log = blob_log(imagen_gray, max_sigma=30, num_sigma=10, threshold=0.1)

    # Ajustar el valor de radio multiplicando por sqrt(2)
    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
    return blobs_log

def definir_blobs_imagenes(paths):
    
    blobs = list()
    for p in paths:
        imagen = cv2.imread(p)
        blobs.append(encontrar_blobs(imagen))
    return blobs

def procesar_video(video_path):
    # Cargar los objetos
    paths = ['ImagenesObjetos/Nutella.jpg', 'ImagenesObjetos/Mermelada.jpg', 'ImagenesObjetos/Cacahuete.jpg']
    objetos = [cv2.imread(p) for p in paths]
    matriz_blobs = definir_blobs_imagenes(paths)

    # Inicializar el contador de objetos
    contador_objetos = [0] * len(objetos)

    # Configurar el video
    cap = cv2.VideoCapture(video_path)

    # Obtener la tasa de fotogramas del video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Crear una variable para indicar si el video está en reproducción
    reproduciendo = True

    # Función para contar objetos en un hilo separado
    def contar_objetos():
        nonlocal reproduciendo
        while reproduciendo:
            ret, frame = cap.read()

            if not ret:
                break

            # Buscar blobs en el frame actual
            blobs_frame = encontrar_blobs(frame)

            # Iterar sobre los blobs encontrados
            for i, blobs_objeto in enumerate(matriz_blobs):
                for blob_frame in blobs_frame:
                    # Verificar si el blob actual coincide con el objeto
                    if np.linalg.norm(blob_frame - blobs_objeto, axis=1).min() < 10:
                        # Incrementar el contador correspondiente
                        contador_objetos[i] += 1

                        # Mostrar el objeto en el frame (puedes personalizar esta parte)
                        cv2.putText(frame, f"Objeto {i + 1}", (int(blob_frame[1]), int(blob_frame[0])),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Mostrar el frame actual
            cv2.imshow('Video', frame)

            # Esperar el tiempo correspondiente al intervalo entre objetos (5 segundos)
            time.sleep(5 / fps)

        # Imprimir el contador final
        for i, count in enumerate(contador_objetos):
            print(f"Objeto {i + 1}: {count} veces")

    # Crear un hilo para contar objetos
    hilo_contador = Thread(target=contar_objetos)

    # Iniciar el hilo
    hilo_contador.start()

    # Esperar hasta que se presione la tecla 'q' para detener la reproducción
    while True:
        if cv2.waitKey(1) & 0xFF == ord(' '):
            reproduciendo = False
            break

    # Esperar a que el hilo de conteo termine
    hilo_contador.join()

    # Liberar los recursos
    cap.release()
    cv2.destroyAllWindows()

    # Ruta del video
    video_path = 'ruta_del_video.mp4'

    # Rutas de las imágenes de objetos
    objetos_paths = ['ImagenesObjetos/Nutella.jpg', 'ImagenesObjetos/Mermelada.jpg', 'ImagenesObjetos/Cacahuete.jpg']

    # Procesar el video
    procesar_video(video_path, objetos_paths)
    
# def ver_objetos(calibration_file):
    # # Conectamos la camara y la configuramos
    # picam = Picamera2()
    # picam.preview_configuration.main.size = (500, 300)
    # picam.preview_configuration.main.format = "RGB888"
    # picam.preview_configuration.align()
    # picam.configure("preview")
    # picam.start()
    # matriz_blobs = definir_blobs_imagenes()
    # combinacion_correcta = False
    # # Cargar parámetros de calibración
    # camera_matrix, dist_coeffs = load_calibration_params(calibration_file)
    # while True:
        # frame = picam.capture_array()
        # # Corregimos la distorsión
        # undistorted_frame = undistort_image(frame, camera_matrix, dist_coeffs)
        # for i, blobs_objeto in enumerate(matriz_blobs):
            # for blob_frame in blobs_frame:
                # # Verificar si el blob actual coincide con el objeto
                # if np.linalg.norm(blob_frame - blobs_objeto, axis=1).min() < 10:
                    # # Incrementar el contador correspondiente
                    # contador_objetos[i] += 1

                    # # Mostrar el objeto en el frame (puedes personalizar esta parte)
                    # cv2.putText(frame, f"Objeto {i + 1}", (int(blob_frame[1]), int(blob_frame[0])),
                                # cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # # Mostrar el frame actual
        # cv2.imshow('Video', frame)

procesar_video(0)
