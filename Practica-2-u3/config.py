SERVERS = [ 
    {"name": "Server1", "host": "localhost", "port": 5001, "db_name": "bank1"}, 
    {"name": "Server2", "host": "localhost", "port": 5002, "db_name": "bank2"}, 
    {"name": "Server3", "host": "localhost", "port": 5003, "db_name": "bank3"} 
] 
SHARED_COLLECTION = "accounts"  # Colección compartida en MongoDB 
USE_SHARED_DB = True  # Usar base de datos compartida 
PRIMARY_INDEX = 0          
# Índice del servidor primario (comienza en Server1) 
CONSISTENCY = "strong"     # Tipo de consistencia: "strong" o "eventual" 