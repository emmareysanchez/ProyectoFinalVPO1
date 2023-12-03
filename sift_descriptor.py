import cv2
import numpy as np
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

def sift_matching(img1, img2):
    sift = cv2.SIFT_create()
    
    # Encuentra los puntos clave y descriptores con SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # Utiliza el Matcher de fuerza bruta (Brute-Force Matcher) para encontrar las coincidencias
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Aplica el umbral Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    return kp1, kp2, good_matches

def stream_video(calibration_file):
    picam = Picamera2()
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    # Cargar parámetros de calibración
    camera_matrix, dist_coeffs = load_calibration_params(calibration_file)

    # Cargar la imagen de referencia
    template_image = cv2.imread('ImagenesObjetos/Nutella.jpg', cv2.IMREAD_COLOR)
    h, w = template_image.shape[:2]

  


if __name__ == "__main__":
    calibration_file_path = "parametros_calibracion.npz"
    stream_video(calibration_file_path)
