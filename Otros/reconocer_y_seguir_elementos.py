import cv2
import numpy as np
from picamera2 import Picamera2

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
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_image

def detect_element(frame, templates):
    max_val = -1
    max_loc = None
    detected_object = None

    for i, template in enumerate(templates):
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, current_max_val, _, current_max_loc = cv2.minMaxLoc(result)

        if current_max_val > max_val:
            max_val = current_max_val
            max_loc = current_max_loc
            detected_object = i  # Guarda el índice del objeto detectado

    threshold = 0.8  # Puedes ajustar este umbral según tus necesidades

    if max_val > threshold:
        return max_loc, detected_object
    else:
        return None, None

def stream_video(calibration_file):
    picam = Picamera2()
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    # Cargar parámetros de calibración
    camera_matrix, dist_coeffs = load_calibration_params(calibration_file)

    if camera_matrix is None or dist_coeffs is None:
        return

    # Cargar las imágenes de referencia
    template_image_nutella = cv2.imread('ImagenesObjetos/Nutella.jpg', cv2.IMREAD_COLOR)
    template_image_mermelada = cv2.imread('ImagenesObjetos/Mermelada.jpg', cv2.IMREAD_COLOR)
    template_image_cacahuete = cv2.imread('ImagenesObjetos/Cacahuete.jpg', cv2.IMREAD_COLOR)

    templates = [template_image_nutella, template_image_mermelada, template_image_cacahuete]

    height, width = template_image_nutella.shape[:2]

    n_imagen = 1
    tracking = False
    tracker = cv2.Tracker_create("MIL")  # Puedes cambiar el tipo de tracker según tus necesidades

    # Contadores para cada objeto
    count_nutella = 0
    count_mermelada = 0
    count_cacahuete = 0

    while True:
        frame = picam.capture_array()

        # Corregir distorsión
        undistorted_frame = undistort_image(frame, camera_matrix, dist_coeffs)

        cv2.imshow("picam", undistorted_frame)

        if not tracking:
            match_location, detected_object = detect_element(undistorted_frame, templates)

            if match_location is not None:
                tracking = True
                tracker.init(undistorted_frame, (match_location[0], match_location[1], width, height))

                # Incrementar el contador del objeto detectado
                if detected_object == 0:
                    count_nutella += 1
                elif detected_object == 1:
                    count_mermelada += 1
                elif detected_object == 2:
                    count_cacahuete += 1
        else:
            success, bbox = tracker.update(undistorted_frame)

            if success:
                x, y, w, h = map(int, bbox)
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            else:
                tracking = False

        key = cv2.waitKey(1) & 0xFF
        if key == ord('h'):
            cv2.imwrite(f'Imagen_circulos{n_imagen}.jpg', frame)
            n_imagen += 1
        elif key == ord('q'):
            break

    # Mostrar el conteo al finalizar
    print("Conteo de objetos:")
    print(f"Nutella: {count_nutella} veces")
    print(f"Mermelada: {count_mermelada} veces")
    print(f"Cacahuete: {count_cacahuete} veces")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    calibration_file_path = "calibration_params.npz"
    stream_video(calibration_file_path)
