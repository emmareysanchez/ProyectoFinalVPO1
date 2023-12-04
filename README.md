# Proyecto Final de la asignatura de Visión por Ordenador
### Integrantes del grupo:
- Emma Rey Sánchez (202110801)
- Catalina Royo-Villanova Seguí (202104665)

## Contenido del repositorio
### Que archivo ejecutar:
- `Controlador.py`: Este fichero de python es el que hay que ejecutar para el funcionamiento del proyecto.
### Archivos soporte
- `conectar_camara_fotos.py`: Fichero de python usado para hacer fotos con la Raspberry Pi 4 y guardarlas. Para hacer una foto hay que ejecutar el fichero y pulsar la tecla **h**.
- `calibracion.py`: Fichero llamado en **Controlador.py** conteniendo el código diseñado para realizar la calibración de la cámara con las imágenes de la carpeta *ImagenesCirculos*.
- `seguridad.py`: Fichero llamado en **Controlador.py** conteniendo el código diseñado para realizar la capa de seguridad. Para introducir un color de la contraseña, hay que pulsar la tecla **espacio**. La contraseña es: "azul, amarillo, rojo, rojo, verde, azul"
- `contador.py`: FFichero llamado en **Controlador.py** conteniendo el código diseñado para encontrar, contar y seguir los objetos de la carpeta *ImagenesObjetos*.
### Recursos utilizados
- `parametros_calibracion.npz`: Archivo conteniendo los parámetros intrínsecos y extrínsecos.
- `ImagenesCirculos`: Carpeta conteniendo las imagenes del tablero circular usadas en la calibración de la cámara.
- `ImagenesObjetos`: Carpeta conteniendo las imagenes de los objetos que reconoceremos y contaremos. Contiene las siguientes fotos:
  - `Nutella.jpg`: Imagen de un tarro de nutella.
  - `Mermelada.png`: Imagen de un tarro de mermelada.
  - `Cacahuete.jpg`: Imagen de un tarro de mantequilla de cacahuete.
