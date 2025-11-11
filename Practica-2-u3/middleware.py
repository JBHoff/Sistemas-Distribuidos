import Pyro5.api
from config import SERVERS, PRIMARY_INDEX, CONSISTENCY 
from utils import log 
import threading 
import time 
import uuid 
class Middleware: 
    def __init__(self): 
        self.servers = [] 
        self.primary_index = PRIMARY_INDEX 
        self.fail_count = 0 
        self.max_retries = 3 
        self.retry_delay = 1 
         
        for s in SERVERS: 
            uri = f"PYRO:{s['name']}@{s['host']}:{s['port']}" 
            self.servers.append(Pyro5.api.Proxy(uri))
    
    def failover(self): 
        self.fail_count += 1 
        if self.fail_count > self.max_retries: 
            log("Todos los servidores fallaron. Operación cancelada.") 
            raise Exception("No hay servidores disponibles") 
        
        log(" Primario caído, seleccionando nuevo primario...") 
        self.primary_index = (self.primary_index + 1) % len(self.servers) 
        log(f" Nuevo primario: {SERVERS[self.primary_index]['name']}") 
        time.sleep(self.retry_delay)

    def propagate_to_replicas_strong(self, method, tx_id, *args): 
        for i, s in enumerate(self.servers): 
            if i != self.primary_index: 
                success = False 
                retries = 0 
                
                while not success and retries < self.max_retries: 
                    try: 
                        getattr(s, method)(*args, tx_id=tx_id) 
                        success = True 
                    except Exception as e: 
                        retries += 1 
                        log(f" {SERVERS[i]['name']} no disponible, reintentando ({retries}/{self.max_retries})") 
                        time.sleep(self.retry_delay) 
                
                if not success: 
                    log(f" No se pudo actualizar {SERVERS[i]['name']} después de {self.max_retries} intentos") 

    def deposit(self, account_id, amount): 
        tx_id = str(uuid.uuid4())  # ID único para esta transacción 
        
        def op(acc_id, amt): 
            return self.get_primary().deposit(acc_id, amt, tx_id) 
        
        result = self._execute_with_failover(op, account_id, amount) 
        self.propagate_to_replicas("deposit", tx_id, account_id, amount) 
        return result
    
    