import asyncio
import socket
import argparse
from PIL import Image
import io

async def send_to_scale_server(image_data):
    """
    Envía la imagen al servidor de escalado y recibe la imagen escalada.

    Parameters:
        image_data (bytes): La imagen en formato de bytes.

    Returns:
        bytes: La imagen escalada en formato de bytes.
    """
    try:
        print("Servidor async: Conectando al servidor de escalado...")
        reader, writer = await asyncio.open_connection('localhost', 8889, family=socket.AF_UNSPEC)
        
        writer.write(image_data)
        await writer.drain()
        print("Servidor async: Imagen enviada al servidor de escalado.")

        scaled_data = await reader.read(10000)
        writer.close()
        await writer.wait_closed()
        print("Servidor async: Imagen escalada recibida del servidor de escalado, tamaño:", len(scaled_data))
        
        return scaled_data
    except Exception as e:
        print(f"Error en conexión con el servidor de escalado: {e}")
        return None

async def handle_client(reader, writer):
    """
    Maneja la conexión con el cliente, convierte la imagen a escala de grises y la escala.

    Parameters:
        reader (StreamReader): Lector de datos del cliente.
        writer (StreamWriter): Escritor para enviar datos al cliente.
    """
    try:
        print("Servidor async: Esperando imagen del cliente...")
        data = await reader.read(10000)
        print("Servidor async: Imagen recibida, tamaño:", len(data))
        
        image = Image.open(io.BytesIO(data)).convert("L")
        output = io.BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)
        
        scaled_image_data = await send_to_scale_server(output.read())
        if scaled_image_data:
            writer.write(scaled_image_data)
            await writer.drain()
            print("Servidor async: Imagen procesada enviada al cliente.")
        else:
            print("Servidor async: Error al procesar la imagen.")
        writer.close()
    except Exception as e:
        print(f"Error en servidor async: {e}")

async def main(ip, port):
    """
    Inicia el servidor asincrónico en la IP y puerto especificados.
    """
    server = await asyncio.start_server(handle_client, ip, port, family=socket.AF_UNSPEC)
    print(f"Servidor async ejecutándose en {ip}:{port}")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Servidor asincrónico de procesamiento de imágenes")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha del servidor asincrónico")
    parser.add_argument("-p", "--port", required=True, type=int, help="Puerto de escucha del servidor asincrónico")
    args = parser.parse_args()

    asyncio.run(main(args.ip, args.port))
