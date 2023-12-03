import numpy as np
import cv2
from picamera2 import Picamera2


def load_calibration_params(file_path):
    calibration_data = np.load(file_path)
    camera_matrix = calibration_data['mtx']
    dist_coeffs = calibration_data['dist']
    return camera_matrix, dist_coeffs


def undistort_image(image, camera_matrix, dist_coeffs):
    h, w = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_image


def encontrar_matches(img1, img2):
    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.60*n.distance:
            good.append([m])
    return good, kp1, kp2


def objeto_en_frame(frame, templates):
    matriz_matches = list()
    for i in range(len(templates)):
        matriz_matches.append([i, encontrar_matches(frame, templates[i])])
    matches = [list(), None, None]
    producto = -1
    for i in matriz_matches:
        if len(matches[0]) < len(i[1][0]) and len(i[1][0]) > 20:
            matches = i[1]
            producto = i[0]
    return producto, matches


def dibujar_rectangulo(frame, templates):
    producto, matches_list = objeto_en_frame(frame, templates)
    if producto != -1:
        template = templates[producto]
        matches = matches_list[0]
        kp_frame = matches_list[1]
        kp_template = matches_list[2]
        # Obtener las coordenadas de los keypoints en el frame y el template
        pts_frame = np.float32([kp_frame[m[0].queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        pts_template = np.float32([kp_template[m[0].trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
        # Calcular la homografía entre el frame y el template
        M, _ = cv2.findHomography(pts_template, pts_frame, cv2.RANSAC, 5.0)
    
        # Obtener las esquinas del rectángulo del template
        h, w = template.shape
        pts_template_rect = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    
        # Transformar las esquinas del template al espacio del frame
        pts_frame_rect = cv2.perspectiveTransform(pts_template_rect, M)
    
        # Dibujar el rectángulo alrededor del objeto en el frame
        frame = cv2.polylines(frame, [np.int32(pts_frame_rect)], True, (0, 0, 255), 2)

    return frame, producto


def contar_objetos(calibration_file, templates):
    # Conectamos la camara y la configuramos
    picam = Picamera2()
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    # Cargar parámetros de calibración
    camera_matrix, dist_coeffs = load_calibration_params(calibration_file)
    contador_productos = [0 for _ in range(len(templates))]
    flag_productos = [False for _ in range(len(templates))]
    contador = 0
    while True:
        frame = picam.capture_array()
        # Corregimos la distorsión
        undistorted_frame = undistort_image(frame, camera_matrix, dist_coeffs)
        undistorted_frame, producto = dibujar_rectangulo(undistorted_frame, templates)
        if producto == -1:
            if contador < 2:
                contador += 1
            else:
                flag_productos = [False for _ in range(len(templates))]
                contador = 0
        else:
            if not flag_productos[producto]:
                flag_productos = [False for _ in range(len(templates))]
                contador_productos[producto] += 1
                flag_productos[producto] = True
                print(producto)

        cv2.imshow("picam", undistorted_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print(f'Cantidad de tarros de nutellas: {contador_productos[0]}.')
            print(f'Cantidad de tarros de mermeladas: {contador_productos[1]}.')
            print(f'Cantidad de tarros de mantequillas de cacahuete: {contador_productos[2]}.')
            break


if __name__ == '__main__':
    imgN = cv2.imread('ImagenesObjetos/Nutella.jpg',cv2.IMREAD_GRAYSCALE)
    imgM = cv2.imread('ImagenesObjetos/Mermelada.jpg',cv2.IMREAD_GRAYSCALE)
    imgC = cv2.imread('ImagenesObjetos/Cacahuete.jpg',cv2.IMREAD_GRAYSCALE)
    templates = [imgN, imgM, imgC]
    contar_objetos('parametros_calibracion.npz', templates)