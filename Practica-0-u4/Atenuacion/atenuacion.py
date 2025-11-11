import time, random, threading 
 
def proceso(): 
    while True: 
        if random.random() < 0.2: 
            print(" Proceso falló inesperadamente") 
            raise Exception("Falla simulada") 
        print(" Proceso en ejecución normal...") 
        time.sleep(2) 
 
def monitor(): 
    while True: 
        try: 
            proceso() 
        except Exception as e: 
            print(f" Monitor detectó: {e}") 
            print(" Reiniciando proceso en 3 segundos...") 
            time.sleep(3) 
 
if __name__ == "__main__": 
    threading.Thread(target=monitor).start()