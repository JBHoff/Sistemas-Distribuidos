import Pyro5.api
import time
from utils import validar_coordenadas

def main():
    # 🔹 IP y puerto del servidor central (en la misma máquina)
    server_ip = "192.168.1.5"

    # 🔹 Conectarse al Name Server local
    ns = Pyro5.api.locate_ns(host=server_ip)
    uri = ns.lookup("servidor.central")
    servidor = Pyro5.api.Proxy(uri)

    print()
    lat_cliente = float(input(" Ingresa tu latitud (ej. 19.4340): "))
    lon_cliente = float(input(" Ingresa tu longitud (ej. -99.1320): "))
    id_cliente = input(" ID del cliente: ")

    validar_coordenadas(lat_cliente, lon_cliente)

    print(" Solicitando vehículo cercano...")
    inicio = time.time()
    vehiculo = servidor.encontrar_vehiculo_cercano(lat_cliente, lon_cliente)
    fin = time.time()

    if vehiculo:
        print(f" Vehículo asignado: {vehiculo}")
        print(f" Tiempo de respuesta: {fin - inicio:.4f} s")
        input(" Presiona ENTER cuando finalice el viaje... ")
        servidor.liberar_vehiculo(vehiculo)
        print(f" Vehículo {vehiculo} liberado. Gracias por usar el servicio.\n")
    else:
        print(" No se encontró vehículo disponible.\n")

if __name__ == "__main__":
    main()