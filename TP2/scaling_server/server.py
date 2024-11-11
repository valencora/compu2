import socketserver
import multiprocessing
from PIL import Image
import io

def scale_image(data, scale_factor=0.5):
    """
    Escala la imagen recibida al tamaño especificado por scale_factor.

    Parameters:
        data (bytes): La imagen en formato de bytes.
        scale_factor (float): El factor de escala de la imagen.

    Returns:
        bytes: La imagen escalada en formato de bytes.
    """
    try:
        image = Image.open(io.BytesIO(data))
        width, height = image.size
        scaled_image = image.resize((int(width * scale_factor), int(height * scale_factor)))
        
        output = io.BytesIO()
        scaled_image.save(output, format='JPEG')
        output.seek(0)
        return output.read()
    except Exception as e:
        print(f"Error escalando la imagen: {e}")
        return None

class ScaleRequestHandler(socketserver.BaseRequestHandler):
    """
    Clase que maneja las solicitudes de escalado de imágenes.
    """

    def handle(self):
        """
        Método que recibe una imagen, la escala y la envía de vuelta.
        """
        try:
            print("Servidor de escalado: Recibiendo imagen para escalado...")
            data = self.request.recv(10000)
            if data:
                scaled_image = scale_image(data, scale_factor=0.5)
                if scaled_image:
                    print("Servidor de escalado: Imagen escalada, enviando de vuelta...")
                    self.request.sendall(scaled_image)
                else:
                    print("Servidor de escalado: Error al procesar la imagen.")
        except Exception as e:
            print(f"Error en el servidor de escalado: {e}")

def start_scaling_server():
    """
    Inicia el servidor de escalado en localhost:8889.
    """
    with socketserver.TCPServer(('localhost', 8889), ScaleRequestHandler) as server:
        print("Servidor de escalado ejecutándose en localhost:8889")
        server.serve_forever()

if __name__ == '__main__':
    process = multiprocessing.Process(target=start_scaling_server)
    process.start()
    process.join()
