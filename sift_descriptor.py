import numpy as np
import cv2
from picamera2 import Picamera2
import glob


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
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = [m for m, n in matches if m.distance < 0.60 * n.distance]
    return good, kp1, kp2


def objeto_en_frame(frame, templates):
    matches_list = []
    for i, template in enumerate(templates):
        matches = encontrar_matches(frame, template)
        matches_list.append([i, matches])
    for i in matches_list:
        print([i[0], len(i[1][0])])
    print('-----')
    matches_list.sort(key=lambda x: len(x[1][0]), reverse=True)
    producto, matches = matches_list[0][0], matches_list[0][1]
    if len(matches[0]) < 15:
        producto, matches = -1, [[], None, None]
    return producto, matches


def dibujar_rectangulo(frame, templates):
    producto, matches_list = objeto_en_frame(frame, templates)
    if producto != -1:
        template = templates[producto]
        matches = matches_list[0]
        kp_frame = matches_list[1]
        kp_template = matches_list[2]
        # Obtener las coordenadas de los keypoints en el frame y el template
        pts_frame = np.float32([kp_frame[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        pts_template = np.float32([kp_template[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
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

  


if __name__ == "__main__":
    calibration_file_path = "parametros_calibracion.npz"
    camera_matrix, dist_coeffs = load_calibration_params(calibration_file_path)
    templates = [cv2.imread('ImagenesObjetos/Mermelada.png',cv2.IMREAD_GRAYSCALE), cv2.imread('ImagenesObjetos/Mermelada2.png',cv2.IMREAD_GRAYSCALE)]
    imagenes = [cv2.imread(p, cv2.IMREAD_GRAYSCALE) for p in glob.glob(f'Imagen_mermelada*.jpg')]
    for frame in imagenes:
        undistorted_frame = undistort_image(frame, camera_matrix, dist_coeffs)
        dibujar_rectangulo(undistorted_frame, templates)
