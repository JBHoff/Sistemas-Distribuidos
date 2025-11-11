# Cliente 2 Server con reintentos ante fallos de comunicación (C2S.py)
import random, time 
def servidor(mensaje): 
    if random.random() < 0.3: 
        raise ConnectionError(" Mensaje perdido") 
    return f"ACK: recibido '{mensaje}'" 
 
def cliente(): 
    for i in range(5): 
        mensaje = f"Petición {i+1}" 
        while True: 
            try: 
                print(f" Enviando: {mensaje}") 
                resp = servidor(mensaje) 
                print(f" Respuesta: {resp}") 
                time.sleep(1)
                break 
            except ConnectionError as e: 
                print(f" {e}. Reintentando...") 
                time.sleep(1) 
 
if __name__ == "__main__": 
    cliente()