# Cliente que interactúa con el middleware: 
import Pyro5.api 
from shared import PYRO_HOST, PYRO_PORT 
 
URI = f"PYRO:middleware@{PYRO_HOST}:{PYRO_PORT}" 
 
def write_key(key, value): 
    try: 
        mw = Pyro5.api.Proxy(URI) 
        res = mw.write(key, value) 
        mw._pyroRelease() 
        return res 
    except Exception as e: 
        return f"Error en escritura: {e}" 
 
def read_key(key): 
    try: 
        mw = Pyro5.api.Proxy(URI) 
        val = mw.read(key) 
        mw._pyroRelease() 
        return val 
    except Exception as e: 
        return f"Error en lectura: {e}" 
 
def main(): 
    print("[client] Cliente Pyro5 listo") 
 
    while True: 
        cmd = input("\nEscribe 'r' para leer, 'w' para escribir, 'q' para salir: ").strip().lower() 
        if cmd == "w": 
            key = input("Clave: ").strip() 
            value = input("Valor: ").strip() 
            res = write_key(key, value) 
            print("Middleware respondió:") 
            for r in res: 
                print("  ", r) 
        elif cmd == "r": 
            key = input("Clave: ").strip() 
            val = read_key(key) 
            print("Valor leído:", val) 
        elif cmd == "q": 
            break 
        else: 
            print("Comando no reconocido.") 
if __name__ == "__main__": 
    main()