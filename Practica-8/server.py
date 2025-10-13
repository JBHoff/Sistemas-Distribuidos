import Pyro5.api 
from utils import distancia_geo, validar_coordenadas 
 
@Pyro5.api.expose 
class ServidorCentral: 
    def __init__(self): 
        self.vehiculos = {} 
        print(" Servidor central iniciado") 
 
    def registrar_vehiculo(self, id_vehiculo, lat, lon): 
        validar_coordenadas(lat, lon) 
        if id_vehiculo not in self.vehiculos: 
            self.vehiculos[id_vehiculo] = {"lat": lat, "lon": lon, "ocupado": False} 
            print(f" Vehículo {id_vehiculo} registrado en ({lat}, {lon}) [Disponible]") 
        else: 
            self.vehiculos[id_vehiculo]["lat"] = lat 
            self.vehiculos[id_vehiculo]["lon"] = lon 
        return True 
 
    def encontrar_vehiculo_cercano(self, lat_cliente, lon_cliente): 
        validar_coordenadas(lat_cliente, lon_cliente) 
        print("\n Vehículos registrados:", self.vehiculos) 
 
        vehiculo_cercano = None 
        distancia_minima = float("inf") 
        radio_maximo_km = 5 
 
        for id_vehiculo, datos in self.vehiculos.items(): 
            if not datos["ocupado"]: 
                dist = distancia_geo((lat_cliente, lon_cliente), (datos["lat"], datos["lon"])) 
                if dist < distancia_minima and dist <= radio_maximo_km: 
                    vehiculo_cercano = id_vehiculo 
                    distancia_minima = dist 
 
        if vehiculo_cercano: 
            self.vehiculos[vehiculo_cercano]["ocupado"] = True 
            print(f" Vehículo {vehiculo_cercano} asignado (distancia {distancia_minima:.2f} km)") 
            return vehiculo_cercano 
        else: 
            print(" No hay vehículos disponibles en el radio") 
            return None 
 
    def liberar_vehiculo(self, id_vehiculo): 
        if id_vehiculo in self.vehiculos: 
            self.vehiculos[id_vehiculo]["ocupado"] = False 
            print(f" Vehículo {id_vehiculo} liberado") 
            return True 
        return False 
 
def main(): 
    daemon = Pyro5.api.Daemon(host="192.168.1.53",port=9090) 
    ns = Pyro5.api.locate_ns(host="192.168.1.53",port=9090) 
#    ns = Pyro5.api.locate_ns()
    uri = daemon.register(ServidorCentral()) 
    ns.register("servidor.central", uri) 
    print(" Servidor registrado en Name Server como 'servidor.central'") 
    daemon.requestLoop() 
 
if __name__ == "__main__": 
    main()