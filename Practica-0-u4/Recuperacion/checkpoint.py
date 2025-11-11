import json, os, time, random 
 
STATE_FILE = "estado.json" 
 
def guardar_estado(contador): 
    with open(STATE_FILE, "w") as f: 
        json.dump({"contador": contador}, f) 
    print(f" Estado guardado: {contador}") 
 
def cargar_estado(): 
    if os.path.exists(STATE_FILE): 
        with open(STATE_FILE, "r") as f: 
            return json.load(f)["contador"] 
    return 0 
 
contador = cargar_estado() 
print(f" Estado inicial: {contador}") 
 
try: 
    while True: 
        contador += 1 
        print(f"Procesando: {contador}") 
        guardar_estado(contador) 
        if random.random() < 0.2: 
            raise Exception(" Falla simulada") 
        time.sleep(1) 
except Exception as e: 
    print(f" {e}") 
    print(" Recuperando desde último estado...") 
    print(f" Estado restaurado: {cargar_estado()}")