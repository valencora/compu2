# Proyecto TP2 - Procesamiento de Imágenes 

## Descripción

Este proyecto es una aplicación distribuida que incluye:
- Un **servidor asincrónico** que recibe imágenes, las convierte a escala de grises y las envía a un segundo servidor para ser escaladas.
- Un **servidor de escalado** que redimensiona las imágenes recibidas y las devuelve al servidor asincrónico.
- Un **cliente** que envía imágenes al servidor asincrónico para procesarlas.

La aplicación está diseñada para manejar múltiples conexiones de manera eficiente utilizando `asyncio` para la concurrencia asíncrona y `multiprocessing` para ejecutar cada servidor en un proceso separado.

## Requisitos

- Python 3.10
- Pillow

## Instalación

1. Crear un entorno virtual:

```bash
python3 -m venv env
source env/bin/activate
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
TP2/
├── async_server/
│   ├── __init__.py
│   └── server.py               # Código del servidor asincrónico
├── scaling_server/
│   ├── __init__.py
│   └── server.py               # Código del servidor de escalado
├── client.py                   # Cliente que envía imágenes al servidor asincrónico
├── tp2.py                      # Script principal que inicia ambos servidores
└──prueba.jpeg                 # Imagen de prueba
```

## Ejecución

### Paso 1: Asegúrate de tener la imagen de prueba

Asegúrate de tener una imagen llamada `prueba.jpeg` en el directorio raíz del proyecto (`TP2/`) o cualquier otra imagen que desees procesar. 

### Paso 2: Ejecutar el Servidor

Para iniciar el proyecto, utiliza `tp2.py`, que aceptará la dirección IP y el puerto para el servidor asincrónico como argumentos. Esto se puede hacer con el siguiente comando:

```bash
python3 tp2.py -i <IP> -p <PORT>
