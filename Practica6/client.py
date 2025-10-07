import Pyro5.api

# ¡IMPORTANTE! Reemplaza "IP_DEL_SERVIDOR" con la dirección IP real de tu computadora servidor.
IP_SERVIDOR = "localhost"  # Por ejemplo: "192.168.1.5"

def mostrar_servicios(ns):
    print("\nLista de servicios disponibles:")
    servicios = ns.list(prefix="ejemplo.")
    for nombre in servicios:
        print(f"- {nombre}")
    return list(servicios.keys())

def cliente_calculadora(calculadora):
    print("\n=== Cliente Calculadora Remota ===")
    while True:
        print("\nOperaciones:\n1. Sumar\n2. Restar\n3. Multiplicar\n4. Dividir\n5. Volver al menú principal")
        opcion = input("Selecciona una opción: ")
        if opcion == "5":
            break
        try:
            a = float(input("Primer número: "))
            b = float(input("Segundo número: "))
        except ValueError:
            print("Entrada no válida.")
            continue
        
        if opcion == "1":
            print("Resultado:", calculadora.sumar(a, b))
        elif opcion == "2":
            print("Resultado:", calculadora.restar(a, b))
        elif opcion == "3":
            print("Resultado:", calculadora.multiplicar(a, b))
        elif opcion == "4":
            print("Resultado:", calculadora.dividir(a, b))
        else:
            print("Opción no válida.")

def cliente_reloj(reloj):
    print("\n=== Cliente Reloj Remoto ===")
    print("Hora actual:", reloj.hora_actual())
    print("Fecha actual:", reloj.fecha_actual())

def main():
    try:
        # Modificación: Conectarse al Name Server usando la IP del servidor.
        ns = Pyro5.api.locate_ns(host=IP_SERVIDOR)
    except Pyro5.errors.NamingError:
        print(f"Error: No se pudo conectar al Name Server en {IP_SERVIDOR}.")
        print("Asegúrate de que el Name Server esté corriendo en el servidor y que la IP sea correcta.")
        return

    while True:
        print("\n=== Cliente Multi-Servicio Pyro5 ===")
        servicios = mostrar_servicios(ns)
        if not servicios:
            print("No hay servicios disponibles. Asegúrate de que el script del servidor esté corriendo.")
            break
        
        opcion = input("\nSelecciona un servicio o escribe 'salir': > ")
        if opcion.lower() == "salir":
            print("Cerrando cliente...")
            break
        
        if opcion not in servicios:
            print("Servicio no encontrado. Intenta de nuevo.")
            continue
        
        uri = ns.lookup(opcion)
        proxy = Pyro5.api.Proxy(uri)
        
        if opcion == "ejemplo.calculadora":
            cliente_calculadora(proxy)
        elif opcion == "ejemplo.reloj":
            cliente_reloj(proxy)
        else:
            print("Servicio sin cliente implementado.")

if __name__ == "__main__":
    main()