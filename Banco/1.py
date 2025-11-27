from middleware import middleware
import sys

def menu_sesion(account_id):
    """Menú que se muestra SOLO cuando lograste entrar"""
    print(f"\n--- 🟢 BIENVENIDO: {account_id} ---")
    while True:
        print("1. Consultar Saldo")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Cerrar Sesión")
        
        op = input(">> ")

        if op == "1":
            bal = middleware.get_balance(account_id)
            print(f"💰 Saldo actual: ${bal}")

        elif op == "2":
            try:
                monto = float(input("Monto a depositar: "))
                nuevo_saldo = middleware.deposit(account_id, monto)
                if nuevo_saldo is not False:
                    print(f"✅ Depósito exitoso. Nuevo saldo: ${nuevo_saldo}")
                else:
                    print("❌ Error en el depósito.")
            except: print("Número inválido")

        elif op == "3":
            try:
                monto = float(input("Monto a retirar: "))
                nuevo_saldo = middleware.withdraw(account_id, monto)
                if nuevo_saldo is not False:
                    print(f"✅ Retiro exitoso. Nuevo saldo: ${nuevo_saldo}")
                else:
                    print("❌ Fondos insuficientes o error.")
            except: print("Número inválido")

        elif op == "4":
            middleware.logout(account_id)
            print("🔒 Sesión cerrada.")
            break

def menu_principal():
    while True:
        print("\n=== 🏦 BANCO DISTRIBUIDO (Postgres) ===")
        print("1. Crear Cuenta Nueva")
        print("2. Iniciar Sesión")
        print("q. Salir")
        
        op = input("Selecciona: ")

        if op == "1":
            acc = input("ID Cuenta (ej. 101): ")
            nom = input("Nombre Titular: ")
            try:
                bal = float(input("Saldo Inicial: "))
                if middleware.create_account(acc, nom, bal):
                    print(f"✅ Cuenta {acc} creada correctamente.")
                else:
                    print("❌ Error: La cuenta ya existe.")
            except: print("Saldo inválido")

        elif op == "2":
            acc = input("Ingresa tu ID de cuenta: ")
            estado = middleware.login(acc)
            
            if estado == "OK":
                try:
                    menu_sesion(acc)
                except KeyboardInterrupt:
                    middleware.logout(acc)
                    print("\nSesión cerrada forzosa.")
                    break
            elif estado == "LOCKED":
                print(f"⛔ ACCESO DENEGADO: La cuenta {acc} ya está abierta en otro dispositivo.")
            elif estado == "NOT_FOUND":
                print("❌ La cuenta no existe.")
            else:
                print("❌ Error de conexión.")

        elif op == "q":
            print("Adiós.")
            break

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\nSaliendo...")