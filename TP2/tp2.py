import multiprocessing
import argparse
import os
import time

def start_scaling_server():
    """
    Inicia el servidor de escalado.
    """
    os.system("python3 scaling_server/server.py")

def start_async_server(ip, port):
    """
    Inicia el servidor asincrónico con la dirección y el puerto especificados.
    """
    os.system(f"python3 async_server/server.py -i {ip} -p {port}")

def main():
    # Configuración de argparse para aceptar parámetros de línea de comandos
    parser = argparse.ArgumentParser(
        description="Tp2 - procesa imágenes",
        usage="tp2.py [-h] -i IP -p PORT"
    )
    parser.add_argument(
        "-i", "--ip", required=True, help="Dirección de escucha"
    )
    parser.add_argument(
        "-p", "--port", required=True, type=int, help="Puerto de escucha"
    )
    args = parser.parse_args()

    # Inicia el servidor de escalado en un proceso separado
    scaling_server_process = multiprocessing.Process(target=start_scaling_server)
    scaling_server_process.start()
    print("Servidor de escalado iniciado en un proceso separado.")

    # Espera un momento para asegurarse de que el servidor de escalado esté en funcionamiento
    time.sleep(1)

    # Inicia el servidor asincrónico en otro proceso con los argumentos de IP y puerto
    async_server_process = multiprocessing.Process(target=start_async_server, args=(args.ip, args.port))
    async_server_process.start()
    print(f"Servidor asincrónico iniciado en {args.ip}:{args.port} en un proceso separado.")

    # Espera a que ambos servidores terminen (lo cual no debería ocurrir a menos que se interrumpan manualmente)
    scaling_server_process.join()
    async_server_process.join()

if __name__ == "__main__":
    main()
