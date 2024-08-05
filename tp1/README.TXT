TP1
Para ejecutar adecuadaente el programa, se debe: 

Para instalar las siguientes librerías:

    pillow==10.3.0
    numpy==2.0.0
    scipy==1.14.0

puedes utilizar el siguiente comando: $ pip3 install -r requirements.txt.

Luego, se debe ejecutar el archivo tpcompu.py con el comando:

$ python3 tpcompu.py ruta/a/tu/imagen.jpg --num_parts 4

El parámetro num_parts determina el número de partes en las que se desea dividir la imagen (puede ser 4 o 2).

El programa se ejecutará en la consola y mostrará la salida tanto en la consola como en formato de imagen (original y con los filtros aplicados).