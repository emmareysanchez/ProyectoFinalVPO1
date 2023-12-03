from calibracion import calibracion
from seguridad import introducir_codigo
# from deteccion_blobs import contar_elementos

if __name__ == '__main__':
    nombre = calibracion()
    introducir_codigo(nombre)
    print('FIN DE LA PRUEBA')
    # n_nutella, n_mermelada, n_cacahuete = contar_elementos()