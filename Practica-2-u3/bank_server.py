from asyncio import start_server
import Pyro5.api
from pymongo import MongoClient
from config import SERVERS, SHARED_COLLECTION, USE_SHARED_DB
from utils import log

@Pyro5.api.expose
class BankServer:
    def __init__(self, db_name):
        self.client = MongoClient("mongodb://localhost:27017/")

        if USE_SHARED_DB:
            self.db = self.client["shared_bank_Sys"]
            self.accounts = self.db[SHARED_COLLECTION]  # Corregido: self.collection -> self.accounts
        else:
            self.db = self.client[db_name]
            self.accounts = self.db["accounts"]  # Corregido: self.collection -> self.accounts
        
        log(f"Conectado a {self.db.name}.{self.accounts.name}")

    def create_account(self, account_id, name, balance):
        try:
            # Verificar si la cuenta ya existe
            if self.accounts.find_one({"Id": account_id}):
                log(f"La cuenta ya existe: {account_id}")
                return False
                
            self.accounts.insert_one({
                "Id": account_id,
                "name": name,
                "balance": balance,
                "tx_ids": []
            })
            log(f"Cuenta creada: {account_id}, {name}, {balance}")
            return True
        except Exception as e:
            log(f"Error al crear cuenta: {e}")
            return False
    
    def deposit(self, account_id, amount, tx_id=None):
        acc = self.accounts.find_one({"Id": account_id})  # Corregido: "Id" en lugar de "_id"
        if not acc:
            log(f"Cuenta no encontrada: {account_id}")
            return False
        
        # Verificar si la transacción ya fue procesada
        if tx_id and tx_id in acc.get("tx_ids", []):
            log(f"Transacción ya procesada: {tx_id} para cuenta {account_id}")
            return acc["balance"]
        
        self.accounts.update_one(
            {"Id": account_id},  # Corregido: "Id" en lugar de "_id"
            {
                "$inc": {"balance": amount},
                "$push": {"tx_ids": tx_id} if tx_id else {}
            }
        )

        new_balance = acc["balance"] + amount
        log(f"Depósito realizado: {amount} a cuenta {account_id}, nuevo balance: {new_balance}")
        return new_balance
    
    def withdraw(self, account_id, amount, tx_id=None): 
        acc = self.accounts.find_one({"Id": account_id})  # Corregido: "Id" en lugar de "_id"
        if not acc or acc["balance"] < amount: 
            log(f"Retiro fallido {amount} en cuenta {account_id}") 
            return False 
        
        # Verificar si la transacción ya fue aplicada 
        if tx_id and tx_id in acc.get("tx_ids", []): 
            log(f"Transacción {tx_id} ya aplicada. Ignorando.") 
            return acc["balance"] 
        
        self.accounts.update_one( 
            {"Id": account_id},  # Corregido: "Id" en lugar de "_id"
            {"$inc": {"balance": -amount}, "$push": {"tx_ids": tx_id}} 
        ) 
        new_balance = acc["balance"] - amount
        log(f"Retiro {amount} en cuenta {account_id} (tx: {tx_id}), nuevo balance: {new_balance}") 
        return new_balance

    def get_balance(self, account_id):
        acc = self.accounts.find_one({"Id": account_id})
        if acc:
            return acc["balance"]
        else:
            log(f"Cuenta no encontrada para consulta de balance: {account_id}")
            return None

    def transfer(self, from_account, to_account, amount, tx_id=None):
        # Esta función podría ser útil para transferencias entre cuentas
        if self.withdraw(from_account, amount, tx_id) is not False:
            if self.deposit(to_account, amount, tx_id) is not False:
                log(f"Transferencia exitosa: {amount} de {from_account} a {to_account}")
                return True
            else:
                # Revertir el retiro si el depósito falla
                self.deposit(from_account, amount, f"rollback_{tx_id}")
                log(f"Transferencia fallida: no se pudo depositar en {to_account}")
        return False

def start_server(index):  # Corregido: fuera de la clase
    if index >= len(SERVERS):
        log(f"Índice de servidor inválido: {index}. Máximo: {len(SERVERS)-1}")
        return
    
    server = SERVERS[index] 
    daemon = Pyro5.api.Daemon(host=server["host"], port=server["port"])
    
    # Registrar el objeto BankServer
    uri = daemon.register(BankServer(server["db_name"]), server["name"])
    log(f"Servidor {server['name']} iniciado en {server['host']}:{server['port']}")
    log(f"URI del objeto: {uri}")
    
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        log("Servidor detenido por el usuario")
    finally:
        daemon.close()
 
if __name__ == "__main__": 
    import sys 
    
    if len(sys.argv) < 2:
        print("Uso: python bank_server.py <índice_del_servidor>")
        print("Servidores disponibles:")
        for i, server in enumerate(SERVERS):
            print(f"  {i}: {server['name']} - {server['host']}:{server['port']}")
        sys.exit(1)
    
    try:
        idx = int(sys.argv[1])
        start_server(idx)
    except ValueError:
        print("Error: El índice debe ser un número entero")
        sys.exit(1)
    except Exception as e:
        log(f"Error al iniciar el servidor: {e}")
        sys.exit(1)