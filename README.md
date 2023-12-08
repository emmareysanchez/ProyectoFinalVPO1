# Proyecto Final de la asignatura de Visión por Ordenador I
### Integrantes del grupo:
- Emma Rey Sánchez (202110801)
- Catalina Royo-Villanova Seguí (202104665)

## Idea del proyecto
Este proyecto simula la identificación de objetos en una cinta de fabricación, y consta de dos partes principales: la **capa de seguridad**, y la **identificación, seguimiento y conteo de objetos**. Nuestra fábrica produce tres productos distintos que son *Nutella*, *Mermelada de Cereza* y *Mantequilla de Cacahuete*. El sistema propuesto realiza un conteo de la cantidad de cada producto tras reconocerlos, para que la fábrica lleve un registro activo de cuánto se produce.

## Contenido del repositorio
### Carpeta de `Codigo`
Contiene el código desarrollado para la realización del proyecto final de la asignatura. A continuación se nombran todos los archivos de la carpeta y se explica su funcionalidad.
#### Que archivos de Python ejecutar:
1. `conectar_camara_fotos.py`: Este archivo de python se usa para hacer fotos con la Raspberry Pi 4 y guardarlas en la carpeta *ImagenesCalibracion*. Es el primero que hay que ejecutar ya que son necesarias las imagenes del patrón de calibración para la calibración de la cámara y posteriormente para desdistorsionar el video recogido con esta. Para hacer una foto hay que ejecutar el fichero y pulsar la tecla **h**.
2. `Controlador.py`: Una vez están las imagenes del patrón guardadas bajo el nombre correcto, se ejecuta este fichero de python que pondrá en funcionamiento el proyecto. Primero hacer la calibración de la cámara, después pasa a la capa de seguridad y cuando se introduce la contraseña correcta en esta, para a la identificación, seguimiento y conteo de objetos.
#### Archivos de Python soporte
- `calibracion.py`: Fichero llamado en **Controlador.py** conteniendo el código diseñado para realizar la calibración de la cámara con las imágenes de la carpeta *ImagenesCalibracion*.
- `seguridad.py`: Fichero llamado en **Controlador.py** conteniendo el código diseñado para realizar la capa de seguridad. Para introducir un color de la contraseña, hay que pulsar la tecla **espacio**. La contraseña es: "azul, rojo, rojo, verde, azul"
- `contador.py`: Fichero llamado en **Controlador.py** conteniendo el código diseñado para encontrar, contar y seguir los objetos de la carpeta *ImagenesObjetos*.
#### Otros archivos usados
- `parametros_calibracion.npz`: Archivo conteniendo la matriz de intrínsecos y los coeficientes de distorsión de la cámara.
- `ImagenesCalibracion`: Carpeta conteniendo las 20 imagenes del tablero circular usadas en la calibración de la cámara.
- `ImagenesObjetos`: Carpeta conteniendo las imagenes de los objetos que reconoceremos y contaremos. Contiene las siguientes fotos:
  - `Nutella.jpg`: Imagen de un tarro de nutella.
  - `Mermelada.png`: Imagen de un tarro de mermelada de cereza.
  - `Cacahuete.jpg`: Imagen de un tarro de mantequilla de cacahuete.


### Carpeta de `Recursos`
- `ImprimirImagenes.pdf`: PDF conteniendo las imagenes usadas para pasar el control de seguridad y realizar el traking de los objetos.
- `PatronCalibracion.pdf`: PDF conteniendo el patrón de calibración utilizado. Contiene 20 círculos distribuidos en 4 filas y 5 columnas de tal forma que los centros de estos están separados por 5 cm de distancia.
- `Informe.pdf`: PDF conteniendo el informe del proyecto.
- `DiagramaProyecto.png`: Imagen del diagrama de bloques del sistema desarrollado.
- `VideoDemo.mkv`: Video de ejemplo mostrando el funcionamiento general del proyecto.
