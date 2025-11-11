import time, random 
 
def ping_servidor(): 
    delay = random.uniform(0.1, 3.0) 
    time.sleep(delay) 
    return delay 
 
for i in range(6): 
    print(f"\nIntento {i+1}") 
    try: 
        t = ping_servidor() 
        if t > 2: 
            raise TimeoutError(f" Tiempo excedido: {t:.2f}s (Falla detectada)") 
        print(f" Respuesta en {t:.2f}s") 
    except TimeoutError as e: 
        print(e)