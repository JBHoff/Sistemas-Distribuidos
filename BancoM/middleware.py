# middleware.py
import Pyro5.api
import threading
import time
from utils import log
#
#SERVERS = [
#    {"name": "Server1", "host": "192.168.1.10", "port": 5001},
#    {"name": "Server2", "host": "192.168.1.11", "port": 5002},
#    {"name": "Server3", "host": "192.168.1.12", "port": 5003},
#]  
#
SERVERS = [
    {"name": "Server1", "host": "server1", "port": 5001},
    {"name": "Server2", "host": "server2", "port": 5002},
    {"name": "Server3", "host": "server3", "port": 5003},
]

class Middleware:
    def __init__(self):
        self.servers = []
        self.primary = 0
        self.active_sessions = {}

        for s in SERVERS:
            uri = f"PYRO:bank@{s['host']}:{s['port']}"
            self.servers.append(Pyro5.api.Proxy(uri))

        threading.Thread(target=self.heartbeat, daemon=True).start()

    # --------------------------
    # CONTROL DE CONCURRENCIA
    # --------------------------
    def login(self, account_id, client_id):
        if account_id in self.active_sessions:
            return f"Cuenta {account_id} está siendo usada por otro cliente."
        
        self.active_sessions[account_id] = client_id
        return f"Conectado a cuenta {account_id}"

    def logout(self, account_id, client_id):
        if self.active_sessions.get(account_id) == client_id:
            del self.active_sessions[account_id]
            return "Sesión cerrada."
        return "No tienes acceso a esta cuenta."

    # --------------------------
    # OPERACIONES BANCARIAS
    # --------------------------
    def deposit(self, account_id, amount):
        try:
            resp = self.servers[self.primary].deposit(account_id, amount)

            # replicación simple a los demás
            for i, srv in enumerate(self.servers):
                if i != self.primary:
                    try:
                        srv.replicate_deposit(account_id, amount)
                    except:
                        pass

            return resp
        except:
            log("Primario caído. Activando failover...")
            self.failover()
            return "Primario falló. Intenta de nuevo."

    # --------------------------
    # HEARTBEAT / MONITOREO
    # --------------------------
    def heartbeat(self):
        while True:
            for i, s in enumerate(self.servers):
                try:
                    s._pyroBind()
                except:
                    log(f"{SERVERS[i]['name']} no responde.")
            time.sleep(5)

    # --------------------------
    # FAILOVER
    # --------------------------
    def failover(self):
        for i in range(len(self.servers)):
            try:
                self.servers[i]._pyroBind()
                self.primary = i
                log(f"{SERVERS[i]['name']} es ahora el primario.")
                return
            except:
                pass

        log("No hay servidores disponibles.")
