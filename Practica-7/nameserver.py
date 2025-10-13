import Pyro5.nameserver 
 
if __name__ == "__main__": 
    print("Iniciando Name Server...") 
    Pyro5.nameserver.start_ns_loop(host="172.20.10.9", port=9090)

#   Pyro5.nameserver.start_ns_loop()  # Usa localhost y puerto por defecto