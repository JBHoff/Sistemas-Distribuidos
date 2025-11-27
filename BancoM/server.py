# server.py
import Pyro5.api
import schedule
import time
import os
import sys
from utils import log

# -------------------------------------------------------------------
# SERVIDOR BANCARIO
# -------------------------------------------------------------------
@Pyro5.api.expose
class BankServer:
    def __init__(self, db_name):
        self.db_name = db_name
        self.accounts = {}   # Puedes reemplazar esto por MongoDB si quieres

    # ------------------------------
    # OPERACIÓN PRINCIPAL: DEPÓSITO
    # ------------------------------
    def deposit(self, account, amount):
        self.accounts[account] = self.accounts.get(account, 0) + amount
        log(f"[PRIMARIO] Depósito en cuenta {account}: +{amount}")
        return f"Depósito exitoso. Nuevo saldo = {self.accounts[account]}"

    # ------------------------------
    # REPLICACIÓN DE DEPÓSITOS
    # ------------------------------
    def replicate_deposit(self, account, amount):
        self.accounts[account] = self.accounts.get(account, 0) + amount
        log(f"[RÉPLICA] Depósito replicado en cuenta {account}: +{amount}")
        return True


# -------------------------------------------------------------------
# BACKUP AUTOMÁTICO 02:00 AM
# -------------------------------------------------------------------
def backup_database():
    log("Iniciando backup automático...")

    # Crea directorio si no existe (Docker lo monta de todos modos)
    os.makedirs("/backups", exist_ok=True)

    # Dump MongoDB si fuera necesario, aquí es demostrativo
    backup_dir = "/backups/" + time.strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(backup_dir, exist_ok=True)

    # Como usamos un diccionario en memoria, simulamos un archivo de respaldo
    with open(f"{backup_dir}/backup.txt", "w") as f:
        f.write("Backup realizado correctamente.\n")

    log("Backup completado.")


# Programación del backup
schedule.every().day.at("02:00").do(backup_database)


# -------------------------------------------------------------------
# SERVIDOR PYRO
# -------------------------------------------------------------------
def run_server(host, port, db):
    daemon = Pyro5.api.Daemon(host=host, port=port)

    bank_obj = BankServer(db)
    uri = daemon.register(bank_obj, "bank")

    print(f"[SERVER READY] {db} escuchando en {host}:{port}")
    print(f"URI: {uri}")

    # Hilo para la ejecución de tareas programadas (backups)
    def schedule_thread():
        while True:
            schedule.run_pending()
            time.sleep(1)

    import threading
    threading.Thread(target=schedule_thread, daemon=True).start()

    daemon.requestLoop()


# -------------------------------------------------------------------
# MAIN PARA DOCKER
# -------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python3 server.py <host> <port> <db_name>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    db_name = sys.argv[3]

    run_server(host, port, db_name)