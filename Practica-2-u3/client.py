from middleware import *
from utils import log 
def menu(): 
    while True: 
        print("\n--- SISTEMA BANCARIO DISTRIBUIDO ---") 
        print("1. Crear cuenta") 
        print("2. Consultar saldo") 
        print("3. Depositar") 
        print("4. Retirar") 
        print("q. Salir") 
        
        choice = input("Selecciona opción: ") 
        
        if choice == "1": 
            acc = input("ID de cuenta: ") 
            name = input("Nombre: ") 
            bal = float(input("Saldo inicial: ")) 
            middleware.create_account(acc, name, bal) 
        
        elif choice == "2": 
            acc = input("ID de cuenta: ") 
            print("Saldo:", middleware.get_balance(acc)) 
        
        elif choice == "3": 
            acc = input("ID de cuenta: ") 
            amt = float(input("Cantidad a depositar: ")) 
            print("Nuevo saldo:", middleware.deposit(acc, amt)) 
        
        elif choice == "4": 
            acc = input("ID de cuenta: ") 
            amt = float(input("Cantidad a retirar: ")) 
            res = middleware.withdraw(acc, amt) 
            if res is False: 
                print("Saldo insuficiente") 
            else: 
                print("Nuevo saldo:", res) 
        elif choice.lower() == "q": 
            break 