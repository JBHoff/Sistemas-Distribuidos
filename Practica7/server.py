import Pyro5.api 
import threading 
from datetime import datetime 
 
@Pyro5.api.expose 
class TicketServer: 
    def __init__(self, boletos_iniciales): 
        self.boletos = boletos_iniciales 
        self.lock = threading.Lock() 
        self.lamport = 0 
 
    def get_time(self): 
        return datetime.now().isoformat() 
 
    def request_ticket(self, cliente, cantidad, client_lamport): 
        with self.lock: 
            self.lamport = max(self.lamport, client_lamport) + 1 
            print(f"[Server] Petición de {cliente}: {cantidad} boletos | Lamport: {self.lamport}") 
 
            if cantidad <= self.boletos: 
                self.boletos -= cantidad 
                print(f"[Server]  {cliente} reservó {cantidad}. Restantes: {self.boletos}") 
                return True, self.boletos, self.lamport 
            else: 
                print(f"[Server]  {cliente} intentó reservar {cantidad}, no hay suficientes.") 
                return False, self.boletos, self.lamport 
 
def main(): 
    boletos_iniciales = int(input(" Ingrese el número total de boletos disponibles: ")) 
    server = TicketServer(boletos_iniciales) 
 
    daemon = Pyro5.api.Daemon() 
    ns = Pyro5.api.locate_ns() 
    uri = daemon.register(server) 
    ns.register("ticket.server", uri) 
 
    print(f" Servidor listo con {boletos_iniciales} boletos. Esperando clientes...") 
    print(f" Hora del servidor: {datetime.now().strftime('%H:%M:%S')}") 
    daemon.requestLoop() 
 
if __name__ == "__main__": 
    main()