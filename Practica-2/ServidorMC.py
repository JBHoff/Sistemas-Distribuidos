import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes = {}
contador_clientes = 0

def handle_client(conn, addr, id_cliente):
    print(f"Cliente {id_cliente} conectado desde {addr}")
    clientes[id_cliente] = conn
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data or data.lower().strip() == "salir":
                print(f"Cliente {id_cliente} desconectado.")
                break
            print(f"[Cliente {id_cliente}] dice: {data}")
    except ConnectionResetError:
        print(f"Cliente {id_cliente} se desconectó abruptamente.")
    finally:
        clientes.pop(id_cliente, None)
        conn.close()

def enviar_desde_servidor():
    while True:
        opcion = input("\nEscribe el ID del cliente o 'todos': ")
        if opcion.lower().strip() == "salir":
            print("Cerrando servidor...")
            break

        msg = input("Mensaje: ")

        if opcion.lower() == "todos":
            for c in clientes.values():
                try:
                    c.sendall(f"[SERVIDOR] {msg}".encode())
                except:
                    pass
        else:
            try:
                id_cliente = int(opcion)
                if id_cliente in clientes:
                    clientes[id_cliente].sendall(f"[SERVIDOR] {msg}".encode())
                else:
                    print("⚠️ Cliente no encontrado")
            except ValueError:
                print("⚠️ ID inválido")

def main():
    global contador_clientes
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")

        threading.Thread(target=enviar_desde_servidor, daemon=True).start()

        while True:
            conn, addr = server.accept()
            contador_clientes += 1
            threading.Thread(target=handle_client, args=(conn, addr, contador_clientes), daemon=True).start()

if __name__ == "__main__":
    main()