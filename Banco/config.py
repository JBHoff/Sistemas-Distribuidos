# config.py

# 1. BUSCA TU IP REAL
# En la computadora que será el SERVIDOR, abre la terminal (cmd o powershell)
# y escribe "ipconfig". Busca "Dirección IPv4" (ej. 192.168.1.15).
# Escribe esa IP aquí abajo:
IP_DEL_SERVIDOR = "192.168.1.1"  # <--- ¡CAMBIA ESTO POR LA IP REAL DEL SERVIDOR!

# --- CONFIGURACIÓN DE BASE DE DATOS ---
# Esto solo lo usa el script del servidor. 
# Como el servidor y la BD están en la misma PC, dejamos 'localhost'.
POSTGRES_CONFIG = {
    'dbname': 'bank_system',
    'user': 'usuario',
    'password': '1234',
    'host': 'localhost', 
    'port': 5432
}

# --- CONFIGURACIÓN DE RED (PYRO) ---
# Aquí definimos DÓNDE está el servidor en la red.
# Reducimos la lista a 1 solo servidor central.
SERVERS = [
    {
        "name": "bank.server.central", # Nombre único para el objeto
        "host": IP_DEL_SERVIDOR,       # La IP que pusimos arriba (NO localhost)
        "port": 9090                   # Puerto abierto en el firewall
    }
]

# --- CONFIGURACIÓN MIDDLEWARE ---
PRIMARY_INDEX = 0   # Siempre es 0 porque solo hay un servidor
CONSISTENCY = "strong"