import cv2
import numpy as np
from picamera2 import Picamera2

def load_calibration_params(file_path):
    calibration_data = np.load(file_path)
    camera_matrix = calibration_data['camera_matrix']
    dist_coeffs = calibration_data['dist_coeffs']
    return camera_matrix, dist_coeffs

def undistort_image(image, camera_matrix, dist_coeffs):
    h, w = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_image

def detect_element(frame, template):
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8  # Puedes ajustar este umbral según tus necesidades

    if max_val > threshold:
        return max_loc
    else:
        return None

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
    template_image = cv2.imread('ruta_de_tu_imagen_de_referencia.jpg', cv2.IMREAD_COLOR)
    h, w = template_image.shape[:2]

    n_imagen = 1
    tracking = False
    tracker = cv2.Tracker_create("MIL")  # Puedes cambiar el tipo de tracker según tus necesidades

    while True:
        frame = picam.capture_array()

        # Corregir distorsión
        undistorted_frame = undistort_image(frame, camera_matrix, dist_coeffs)

        cv2.imshow("picam", undistorted_frame)

        if not tracking:
            match_location = detect_element(undistorted_frame, template_image)

            if match_location is not None:
                tracking = True
                tracker.init(undistorted_frame, (match_location[0], match_location[1], w, h))
        else:
            success, bbox = tracker.update(undistorted_frame)

            if success:
                x, y, w, h = map(int, bbox)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                tracking = False

        if cv2.waitKey(1) & 0xFF == ord('h'):
            cv2.imwrite(f'Imagen_circulos{n_imagen}.jpg', frame)
            n_imagen += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    calibration_file_path = "calibration_params.npz"
    stream_video(calibration_file_path)
