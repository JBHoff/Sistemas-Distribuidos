import Pyro5.nameserver 
 
if __name__ == "__main__": 
    print("Iniciando Name Server...") 
    Pyro5.nameserver.start_ns_loop()