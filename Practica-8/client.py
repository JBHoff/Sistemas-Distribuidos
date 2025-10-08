import Pyro5.api 
import time 
from utils import validar_coordenadas 
 
def main(): 
    lat = float(input(" Ingresa tu latitud (ej. 19.4340): ")) 
    lon = float(input(" Ingresa tu longitud (ej. -99.1320): ")) 
    validar_coordenadas(lat, lon) 
    id_cliente = input(" ID del cliente: ").strip() 
 
    ns = Pyro5.api.locate_ns() 
#   ns = Pyro5.api.locate_ns()
    uri = ns.lookup("servidor.central") 
    servidor = Pyro5.api.Proxy(uri) 
 
    print(" Solicitando vehículo cercano...") 
    inicio = time.time() 
    vehiculo = servidor.encontrar_vehiculo_cercano(lat, lon) 
    fin = time.time() 
 
    if vehiculo: 
        print(f" Vehículo asignado: {vehiculo}") 
        print(f" Tiempo de respuesta: {fin - inicio:.4f} s") 
        input(" Presiona ENTER cuando finalice el viaje...") 
        servidor.liberar_vehiculo(vehiculo) 
        print(f" Vehículo {vehiculo} liberado. Gracias por usar el servicio.") 
    else: 
        print(" No hay vehículos disponibles.") 
        print(f" Tiempo de respuesta: {fin - inicio:.4f} s") 
 
if __name__ == "__main__": 
    main()