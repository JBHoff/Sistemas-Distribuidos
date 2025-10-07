import requests 
import threading 
import time 
 
SERVER_URL = "http://192.168.1.53:5050" 
 
class ChatClient: 
    def __init__(self): 
        self.usuario = input("Ingresa tu nombre de usuario: ").strip() 
        self.mensajes_vistos = 0 
        self.running = True 
 
    def enviar_mensaje(self, mensaje): 
        try: 
            requests.post(f"{SERVER_URL}/enviar", json={"usuario": self.usuario, "mensaje": 
mensaje}) 
        except Exception as e: 
            print(f"Error al enviar mensaje: {e}") 
 
    def recibir_mensajes(self): 
        while self.running: 
            try: 
                resp = requests.get(f"{SERVER_URL}/recibir") 
                if resp.status_code == 200: 
                    mensajes = resp.json() 
                    nuevos = mensajes[self.mensajes_vistos:] 
                    for m in nuevos: 
                        print(f"[{m['hora']}] {m['usuario']}: {m['mensaje']}") 
                    self.mensajes_vistos = len(mensajes) 
            except Exception as e: 
                print(f"Error al recibir mensajes: {e}") 
            time.sleep(1)  # Actualiza cada 1 segundo 
 
    def run(self): 
        threading.Thread(target=self.recibir_mensajes, daemon=True).start() 
        print("Conectado al chat. Escribe 'salir' para terminar.") 
        while True: 
            msg = input(f"{self.usuario}: ").strip() 
            if msg.lower() == "salir": 
                self.running = False 
                break 
            self.enviar_mensaje(msg) 
 
if __name__ == "__main__": 
    client = ChatClient() 
    client.run()