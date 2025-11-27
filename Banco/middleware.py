import Pyro5.api
import Pyro5.errors
from config import SERVERS, PRIMARY_INDEX
import time

class MiddlewarePostgres:
    def __init__(self):
        self.servers = SERVERS
        self.primary_index = PRIMARY_INDEX
        self.proxies = []
        
        # Crear proxies
        for s in self.servers:
            uri = f"PYRO:{s['name']}@{s['host']}:{s['port']}"
            self.proxies.append(Pyro5.api.Proxy(uri))

    def get_primary(self):
        return self.proxies[self.primary_index]

    def _exec(self, func, *args):
        """Intenta ejecutar en el primario, si falla, cambia al siguiente"""
        max_retries = 3
        attempts = 0
        
        while attempts < max_retries:
            try:
                return func(self.get_primary(), *args)
            except (Pyro5.errors.ConnectionClosedError, Pyro5.errors.CommunicationError):
                print(f"[Middleware] Servidor {self.primary_index} caído. Cambiando...")
                self.primary_index = (self.primary_index + 1) % len(self.servers)
                attempts += 1
                time.sleep(0.5)
        
        raise Exception("Sistema no disponible (todos los servidores caídos)")

    # --- MÉTODOS EXPUESTOS AL CLIENTE ---

    def login(self, account_id):
        return self._exec(lambda s, a: s.login(a), account_id)

    def logout(self, account_id):
        try:
            return self._exec(lambda s, a: s.logout(a), account_id)
        except:
            return False

    def create_account(self, account_id, name, balance):
        return self._exec(lambda s, a, n, b: s.create_account(a, n, b), account_id, name, balance)

    def deposit(self, account_id, amount):
        return self._exec(lambda s, a, m: s.deposit(a, m), account_id, amount)

    def withdraw(self, account_id, amount):
        return self._exec(lambda s, a, m: s.withdraw(a, m), account_id, amount)

    def get_balance(self, account_id):
        return self._exec(lambda s, a: s.get_balance(a), account_id)

# Instancia única
middleware = MiddlewarePostgres()