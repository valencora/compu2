import asyncio
import os
from PIL import Image
import io

async def send_image_to_server(image_path, output_path):
    reader, writer = await asyncio.open_connection('localhost', 8888)
    
    # Lee la imagen y envíala al servidor asincrónico
    with open(image_path, "rb") as f:
        image_data = f.read()

    print("Cliente: Enviando imagen al servidor asincrónico...")
    writer.write(image_data)
    await writer.drain()

    # Recibe la imagen procesada desde el servidor asincrónico
    processed_image_data = await reader.read(10000)  
    print("Cliente: Imagen procesada recibida, tamaño:", len(processed_image_data))

    # Guarda la imagen procesada
    processed_image = Image.open(io.BytesIO(processed_image_data))
    processed_image.save(output_path)
    print(f"Cliente: Imagen procesada guardada en {output_path}")

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "prueba.jpeg")
    output_path = os.path.join(current_dir, "output_image.jpg")

    asyncio.run(send_image_to_server(image_path, output_path))
