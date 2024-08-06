import argparse
from PIL import Image, ImageFilter
import math
import multiprocessing
import signal
import sys

def open_imagen(ruta):
    try:
        # Abre la imagen
        imagen = Image.open(ruta).convert('RGB')
        # Muestra la imagen
        imagen.show()
        # Retorna la imagen
        return imagen
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return None

def split_image(imagen, num_parts):
    width, height = imagen.size
    # Calcular las filas y columnas
    columns = math.ceil(math.sqrt(num_parts))
    rows = math.ceil(num_parts / columns)
    width_part = width // columns
    height_part = height // rows

    parts = []

    for i in range(rows):
        for j in range(columns):
            if len(parts) < num_parts:  # Solo crear partes hasta alcanzar num_parts
                box = (j * width_part, i * height_part, (j + 1) * width_part, (i + 1) * height_part)
                part = imagen.crop(box)
                parts.append(part)
    return parts

def apply_filter(imagen, filter_type):
    filters = {
        'emboss': ImageFilter.EMBOSS
    }
    if filter_type in filters:
        return imagen.filter(filters[filter_type])
    else:
        raise ValueError(f"Filtro no reconocido: {filter_type}")

def worker(index, start, end, width_part, height_part, array, pipe, filter_type):
    try:
        part = Image.frombytes('RGB', (width_part, height_part), bytes(array[start:end]))
        filtered_part = apply_filter(part, filter_type)
        array[start:end] = filtered_part.tobytes()
        pipe.send(index)
    except Exception as e:
        pipe.send((index, str(e)))
    finally:
        pipe.close()

def signal_handler(sig, frame):
    print('Interrupción recibida. Finalizando...')
    sys.exit(0)

def combine_images(width, height, width_part, height_part, num_parts, array):
    columns = math.ceil(math.sqrt(num_parts))
    combined_image = Image.new('RGB', (width, height))

    for index in range(num_parts):
        row = index // columns
        col = index % columns
        start = index * width_part * height_part * 3
        end = (index + 1) * width_part * height_part * 3
        part = Image.frombytes('RGB', (width_part, height_part), bytes(array[start:end]))
        combined_image.paste(part, (col * width_part, row * height_part))

    return combined_image

if __name__ == "__main__":
    # Manejo de señales
    signal.signal(signal.SIGINT, signal_handler)

    # Crear el objeto parser
    parser = argparse.ArgumentParser(description="Abrir y mostrar una imagen, dividirla en partes iguales, y aplicar un filtro a cada parte en paralelo.")

    # Añadir un argumento para la ruta de la imagen
    parser.add_argument('ruta', type=str, help='Ruta del archivo de imagen.')

    # Añadir un argumento opcional para el número total de partes
    parser.add_argument('--num_parts', type=int, default=1, help='Número total de partes en las que dividir la imagen.')

    # Parsear los argumentos
    args = parser.parse_args()

    # Llamar a la función open_imagen con la ruta proporcionada
    imagen = open_imagen(args.ruta)

    if imagen:
        width, height = imagen.size
        # Dividir la imagen en partes iguales
        parts = split_image(imagen, args.num_parts)

        # Crear array compartido
        part_width, part_height = parts[0].size
        total_size = part_width * part_height * 3 * args.num_parts
        part_size = part_width * part_height * 3
        shared_array = multiprocessing.Array('B', total_size)

        # Copiar partes de imagen al array compartido
        for index, part in enumerate(parts):
            start = index * part_size
            end = (index + 1) * part_size
            shared_array[start:end] = part.tobytes()

        # Crear pipes y procesos
        processes = []
        parent_conns = []

        filters = ['emboss']

        for index in range(args.num_parts):
            start = index * part_size
            end = (index + 1) * part_size
            parent_conn, child_conn = multiprocessing.Pipe()
            parent_conns.append(parent_conn)
            filter_type = filters[index % len(filters)]
            p = multiprocessing.Process(target=worker, args=(index, start, end, part_width, part_height, shared_array, child_conn, filter_type))
            processes.append(p)
            p.start()

        # Esperar los resultados
        completed = 0
        while completed < args.num_parts:
            for parent_conn in parent_conns:
                try:
                    result = parent_conn.recv()
                    if isinstance(result, tuple):
                        index, error = result
                        print(f"Error en la parte {index}: {error}")
                    else:
                        completed += 1
                except EOFError:
                    continue

        for p in processes:
            p.join()

        combined_image = combine_images(width, height, part_width, part_height, args.num_parts, shared_array)
        combined_image.show()
