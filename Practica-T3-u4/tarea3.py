import json, os, time, random

LOG_FILE = "wal_log.json"

# --- Funciones básicas del WAL ---
def write_log(entry):
    log = load_log()
    log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)
    print(f"[LOG] {entry}")

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

# --- Participante ---
def participante(vote=True):
    tx_id = random.randint(1000, 9999)
    print(f"\nParticipante inicia TX {tx_id}")

    write_log({"tx": tx_id, "state": "PREPARED"})
    time.sleep(1)

    # Simula fallo o decisión
    if vote:
        write_log({"tx": tx_id, "state": "COMMIT"})
        print("Transacción confirmada")
    else:
        write_log({"tx": tx_id, "state": "ABORT"})
        print("Transacción abortada")

# --- Recuperación tras falla ---
def recovery():
    log = load_log()
    print("\nRecuperando estado desde WAL...")
    for entry in log:
        tx, state = entry["tx"], entry["state"]
        if state == "PREPARED":
            print(f"TX {tx} quedó pendiente, pidiendo decisión al coordinador...")
            # Simulamos que el coordinador responde "commit"
            write_log({"tx": tx, "state": "COMMIT"})
            print(f"TX {tx} marcada como COMMIT tras recuperación")
        elif state == "COMMIT":
            print(f"TX {tx} ya confirmada (redo)")
        elif state == "ABORT":
            print(f"↩TX {tx} abortada (undo)")

# --- Simulación ---
if __name__ == "__main__":
    print("=== Simulador WAL para transacciones distribuidas ===")

    # Simulamos ejecución normal
    participante(vote=random.choice([True, False]))

    # Simulamos un fallo
    print("\nSimulando caída del sistema...")
    time.sleep(1)

    # Recuperación tras reinicio
    recovery()