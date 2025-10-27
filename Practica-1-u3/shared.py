# Archivo de configuración global: 
# shared.py 
# Host donde se ejecutarán las réplicas y el middleware 
PYRO_HOST = "localhost" 
# Puerto donde estará el middleware 
PYRO_PORT = 5000 
 
# URIs de las réplicas 
REPLICA1_URI = "PYRO:replica1@localhost:5001" 
REPLICA2_URI = "PYRO:replica2@localhost:5002" 