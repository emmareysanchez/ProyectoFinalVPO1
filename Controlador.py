from calibracion import calibracion
from seguridad import introducir_codigo
from contador import contar_objetos
import cv2

if __name__ == '__main__':
    imgN = cv2.imread('ImagenesObjetos/Nutella.jpg', cv2.IMREAD_GRAYSCALE)
    imgM = cv2.imread('ImagenesObjetos/Mermelada.jpg', cv2.IMREAD_GRAYSCALE)
    imgC = cv2.imread('ImagenesObjetos/Cacahuete.jpg', cv2.IMREAD_GRAYSCALE)
    templates = [imgN, imgM, imgC]

    fichero_calibracion = calibracion()
    introducir_codigo(fichero_calibracion)
    print('Prueba de seguridad pasada.')

    n_nutella, n_mermelada, n_cacahuete = contar_objetos(fichero_calibracion, templates)
    print(f'Cantidad de tarros de nutellas: {n_nutella}.')
    print(f'Cantidad de tarros de mermeladas: {n_mermelada}.')
    print(f'Cantidad de tarros de mantequillas de cacahuete: {n_cacahuete}.')