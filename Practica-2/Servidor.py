#servidor 
import socket 
import threading 
 
HOST = "192.168.1.2" 
PORT = 5000 
 
def receive_messages(conn): 
    """Hilo para recibir mensajes del cliente""" 
    try: 
        while True: 
            data = conn.recv(1024).decode() 
            if not data or data.lower().strip() == "salir": 
                print("\nCliente desconectado.") 
                break 
            print(f"\nCliente: {data}") 
    except ConnectionResetError: 
        print("\nCliente desconectado abruptamente.") 
    finally: 
        conn.close() 
 
def main(): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: 
        server.bind((HOST, PORT)) 
        server.listen() 
        print(f"Servidor escuchando en {HOST}:{PORT}") 
        conn, addr = server.accept() 
        print(f"Conectado con {addr}") 
 
        # Inicia hilo para recibir mensajes 
        threading.Thread(target=receive_messages, args=(conn,), daemon=True).start() 
 
        # Hilo principal para enviar mensajes 
        try: 
            while True: 
                msg = input("Servidor: ") 
                if msg.lower() == "salir": 
                    conn.sendall(msg.encode()) 
                    print("Cerrando conexión...") 
                    break 
                conn.sendall((msg + "\n").encode()) 
        except Exception as e: 
            print(f"Error: {e}") 
 
if __name__ == "__main__": 
    main()