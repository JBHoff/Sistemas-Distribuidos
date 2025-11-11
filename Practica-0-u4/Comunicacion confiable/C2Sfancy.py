# Cliente 2 Server con reintentos ante fallos de comunicación (C2S.py)
import random, time, sys

def barra_carga(t=1.5):
    #Muestra una barra animada de duración 't' segunún el tiempo dado
    ancho = 25
    pasos = int(ancho)
    for i in range(pasos + 1):
        porcentaje = i / pasos
        llenado = int(porcentaje * ancho)
        barra = "▓" * llenado + "░" * (ancho - llenado)
        sys.stdout.write(f"\r--Esperando respuesta {barra} {porcentaje*100:5.1f}%")
        sys.stdout.flush()
        time.sleep(t / pasos)
    print()  # salto de línea

def servidor(mensaje):
    # 30% de probabilidad de falla
    if random.random() < 0.3:
        raise ConnectionError("Mensaje perdido")
    return f"ACK: recibido '{mensaje}'"

def cliente():
    for i in range(5):
        mensaje = f"Petición {i+1}"
        while True:
            try:
                print(f"\nEnviando: {mensaje}")
                barra_carga(random.uniform(1.0, 2.0))  # espera simulada
                resp = servidor(mensaje)
                print(f"Respuesta: {resp}")
                time.sleep(1)
                break
            except ConnectionError as e:
                print(f"!!!!!!! {e}. Reintentando...\n")
                time.sleep(1)

if __name__ == "__main__":
    cliente()