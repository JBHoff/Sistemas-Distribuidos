import Pyro5.api 
import time 
import random 
from utils import validar_coordenadas 
 
def main(): 
    id_vehiculo = input(" ID del vehículo: ").strip() 
    lat = float(input(" Ingresa tu latitud (ej. 19.4340): ")) 
    lon = float(input(" Ingresa tu longitud (ej. -99.1320): ")) 
    validar_coordenadas(lat, lon) 
 
    ns = Pyro5.api.locate_ns() 
#   ns = Pyro5.api.locate_ns()
    uri = ns.lookup("servidor.central") 
    servidor = Pyro5.api.Proxy(uri) 
 
    print(f" {id_vehiculo} activo. Enviando coordenadas...") 
    while True: 
        servidor.registrar_vehiculo(id_vehiculo, lat, lon) 
        lat += random.uniform(-0.0005, 0.0005) 
        lon += random.uniform(-0.0005, 0.0005) 
        time.sleep(5) 
 
if __name__ == "__main__": 
    main()