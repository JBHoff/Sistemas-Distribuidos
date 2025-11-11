import threading
import time
import random
import sys

def proceso(): 
    while True: 
        if random.random() < 0.2: 
            print("\n Proceso falló inesperadamente") 
            raise Exception("Falla simulada") 
        print(" Proceso en ejecución normal...") 
        time.sleep(2) 

def barra_carga(segundos):
    #Muestra una barra de carga con cuenta regresiva.
    for i in range(segundos, 0, -1):
        sys.stdout.write(f"\r Reiniciando en {i}... ")
        sys.stdout.flush()
        # Simula una barra con caracteres ▓ y ░
        for j in range(10):
            sys.stdout.write("▓")
            sys.stdout.flush()
            time.sleep( (1 / 10) )  # divide el segundo en 10 partes
        sys.stdout.write("  ")
    print("\rReiniciando proceso...\n")

def monitor(): 
    while True: 
        try: 
            proceso() 
        except Exception as e: 
            print(f"Monitor detectó: {e}")
            barra_carga(3)  # cuenta regresiva con barra de 3 segundos

if __name__ == "__main__": 
    threading.Thread(target=monitor).start()
