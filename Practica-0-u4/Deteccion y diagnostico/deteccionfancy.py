import time, random, sys

def barra_tiempo(t, limite=3.0):
    #Muestra una barra animada que dura 't' segundos.
    ancho_barra = 30  # longitud de la barra
    pasos = int(ancho_barra)
    for i in range(pasos + 1):
        porcentaje = i / pasos
        llenado = int(porcentaje * ancho_barra)
        barra = "▓" * llenado + "░" * (ancho_barra - llenado)
        sys.stdout.write(f"\r[{barra}] {porcentaje*100:5.1f}%")
        sys.stdout.flush()
        time.sleep(t / pasos)
    print()  # salto de línea al terminar

def ping_servidor(): 
    delay = random.uniform(0.1, 3.0) 
    barra_tiempo(delay)
    return delay 
 
for i in range(6): #Numero de intentos o demostraciones
    print(f"\n🔹 Intento {i+1}")
    try: 
        t = ping_servidor() 
        if t > 2: 
            raise TimeoutError(f"Tiempo excedido: {t:.2f}s (Falla detectada)") 
        print(f"Respuesta recibida en {t:.2f}s") 
    except TimeoutError as e: 
        print(f"{e}")
