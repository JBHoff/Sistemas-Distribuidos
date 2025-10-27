import Pyro5.api 
import pymongo 
from shared import PYRO_HOST 
 
class Replica: 
    def __init__(self, name, db_name): 
        self.name = name 
        # Conectar a MongoDB local 
        self.client = pymongo.MongoClient("mongodb://localhost:27017/") 
        self.db = self.client[db_name] 
        self.collection = self.db["data"] 
 
    @Pyro5.api.expose 
    def write(self, key, value): 
        """Escribe o actualiza un valor y muestra en consola lo que hace.""" 
        self.collection.update_one( 
            {"key": key}, {"$set": {"value": value}}, upsert=True 
        ) 
        print(f"[{self.name}] Clave '{key}' guardada con valor '{value}'") 
        return f"Replica {self.name}: clave '{key}' guardada." 
 
    @Pyro5.api.expose 
    def read(self, key): 
        """Lee un valor y muestra en consola lo que lee.""" 
        doc = self.collection.find_one({"key": key}) 
        val = doc["value"] if doc else None 
        print(f"[{self.name}] Lectura clave '{key}' -> '{val}'") 
        return val 
 
if __name__ == "__main__": 
    replica = Replica("R1", "replica1_db") 
    daemon = Pyro5.api.Daemon(host=PYRO_HOST, port=5002) 
    uri = daemon.register(replica, objectId="replica1") 
    print(f"Replica1 lista en: {uri}") 
    daemon.requestLoop() 