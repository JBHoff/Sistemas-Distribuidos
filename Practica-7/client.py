import Pyro5.api 
from datetime import datetime 
import time 
 
def cristian_sync(server): 
    t1 = datetime.now() 
    server_time_str = server.get_time() 
    t2 = datetime.now() 
    server_time = datetime.fromisoformat(server_time_str) 
    adjusted_time = server_time + (t2 - t1)/2 
    print(f"[Cristian] RTT: {(t2-t1).total_seconds():.3f}s → Hora ajustada: {adjusted_time.strftime('%H:%M:%S.%f')[:-3]}") 
    return adjusted_time 
 
def berkeley_sync(server_time, client_time): 
    adjusted = client_time + (server_time - client_time)/2 
    diff = (server_time - client_time).total_seconds() 
    offset = diff / 2 
    print(f"[Berkeley] Diferencia: {diff:.3f}s → Offset aplicado: {offset:.3f}s") 
    return adjusted 
 
def main(): 
    cliente = input("Ingrese su nombre de cliente: ") 
    ns = Pyro5.api.locate_ns() 
    uri = ns.lookup("ticket.server") 
    server = Pyro5.api.Proxy(uri) 
 
    client_lamport = 0 
    client_time = datetime.now() 
 
    while True: 
        print(f"\n[{cliente}] Hora actual: {client_time.strftime('%H:%M:%S.%f')[:-3]} | Lamport: {client_lamport}") 
        try: 
            cantidad = int(input("Ingrese cantidad de boletos a reservar (0 para salir): ")) 
        except ValueError: 
            print(" Ingrese un número válido.") 
            continue 
 
        if cantidad == 0: 
            break 
 
        client_time = cristian_sync(server) 
        server_time = datetime.fromisoformat(server.get_time()) 
        client_time = berkeley_sync(server_time, client_time) 
 
        client_lamport += 1 
        success, restantes, server_lamport = server.request_ticket(cliente, cantidad, client_lamport) 
        client_lamport = max(client_lamport, server_lamport) + 1 
 
        if success: 
            print(f"[{cliente}]  Reserva exitosa. Restantes: {restantes}. Lamport: {client_lamport}") 
        else: 
            print(f"[{cliente}]  No hay boletos suficientes. Restantes: {restantes}") 
 
        time.sleep(1) 
 
if __name__ == "__main__": 
    main()