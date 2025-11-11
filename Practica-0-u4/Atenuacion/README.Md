# Toleracia a Fallas
## Practica Intro
### * Objetivo 
    Mostrar cómo un monitor detecta la caída de un proceso y lo reinicia (atenuación de fallas).

### * Explicación línea por línea 
    1. import time, random, threading — importa time (pausas), random (aleatoriedad), threading (hilos). 
    2. def proceso(): — define la función que simula la tarea del proceso. 
    3. while True: — bucle infinito que representa el ciclo de trabajo. 
    4. if random.random() < 0.2: — con 20% de probabilidad se simula una falla. 
    5. print(" Proceso falló inesperadamente") — imprime aviso de falla. 
    6. raise Exception("Falla simulada") — lanza excepción para simular la caída del proceso. 
    7. print(" Proceso en ejecución normal...") — mensaje de ejecución normal. 
    8. time.sleep(2) — simula trabajo esperando 2 segundos. 
    9. def monitor(): — define el monitor que supervisa el proceso. 
    10. while True: — bucle del monitor (siempre en vigilia). 
    11. try: — intenta ejecutar proceso() y atrapar su excepción si falla. 
    12. proceso() — ejecuta la función de trabajo (puede lanzar excepción). 
    13. except Exception as e: — captura la excepción generada por proceso. 
    14. print(f" Monitor detectó: {e}") — imprime diagnóstico de falla. 
    15. print(" Reiniciando proceso en 3 segundos...") — mensaje de reinicio. 
    16. time.sleep(3) — espera 3 segundos antes de reintentar. 
    17. if __name__ == "__main__": — verifica punto de entrada del script. 
    18. threading.Thread(target=monitor).start() — crea y arranca un hilo que ejecuta el monitor en background.