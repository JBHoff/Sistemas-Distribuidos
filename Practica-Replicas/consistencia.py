# consistencia.py
# Simulación de modelos de consistencia en lecturas/escrituras

import random

# Simular réplicas con versiones
replicas = [
    {"name": "R1", "version": 1, "value": 100},
    {"name": "R2", "version": 1, "value": 100},
    {"name": "R3", "version": 1, "value": 100},
]

class Client:
    def __init__(self):
        self.last_read_version = 0
        self.last_write_version = 0

    def read(self):
        # Lecturas monotónicas: solo acepta versiones >= última leída
        valid_replicas = [r for r in replicas if r["version"] >= self.last_read_version]
        if not valid_replicas:
            print("No hay réplicas válidas.")
            return
        replica = max(valid_replicas, key=lambda r: r["version"])
        self.last_read_version = replica["version"]
        print(f"Lectura desde {replica['name']} -> Valor={replica['value']} (v{replica['version']})")

    def write(self, delta):
        # Escrituras monotónicas y Read-your-writes
        new_version = max(r["version"] for r in replicas) + 1
        new_value = replicas[0]["value"] + delta
        master = random.choice(replicas)
        master["version"] = new_version
        master["value"] = new_value
        self.last_write_version = new_version
        print(f"Escritura en {master['name']} -> Valor={new_value} (v{new_version})")

    def write_after_read(self, delta):
        # Las escrituras siguen a las lecturas
        base_version = self.last_read_version
        new_version = base_version + 1
        master = random.choice(replicas)
        master["version"] = new_version
        master["value"] += delta
        print(f"Escritura tras lectura ({master['name']}) -> Valor={master['value']} (v{new_version})")
        self.last_write_version = new_version

# --- Demostración ---
client = Client()
print("\n--- Lecturas monotónicas ---")
client.read()
replicas[1]["version"] = 2  # simula replicación parcial
replicas[1]["value"] = 105
client.read()

print("\n--- Lea sus escrituras ---")
client.write(+10)
client.read()

print("\n--- Escrituras monotónicas ---")
client.write(+5)
client.write(+3)

print("\n--- Las escrituras siguen a las lecturas ---")
client.read()
client.write_after_read(+2)
