# Coordina las escrituras y lecturas entre réplicas: 
import Pyro5.api 
from shared import PYRO_HOST, PYRO_PORT, REPLICA1_URI, REPLICA2_URI, REPLICA3_URI
 
class Middleware: 
    @Pyro5.api.expose 
    def write(self, key, value): 
        responses = [] 
 
        # Replica 1 
        try: 
            r1 = Pyro5.api.Proxy(REPLICA1_URI) 
            print(f"[Middleware] Enviando clave '{key}' -> '{value}' a Replica1") 
            resp1 = r1.write(key, value) 
            print(f"[Middleware] Respuesta de Replica1: {resp1}") 
            responses.append(resp1) 
            r1._pyroRelease() 
        except Exception as e: 
            responses.append(f"Error réplica1: {e}") 
            print(f"[Middleware] Error enviando a Replica1: {e}") 
 
        # Replica 2 
        try: 
            r2 = Pyro5.api.Proxy(REPLICA2_URI) 
            print(f"[Middleware] Enviando clave '{key}' -> '{value}' a Replica2") 
            resp2 = r2.write(key, value) 
            print(f"[Middleware] Respuesta de Replica2: {resp2}") 
            responses.append(resp2) 
            r2._pyroRelease() 
        except Exception as e: 
            responses.append(f"Error réplica2: {e}") 
            print(f"[Middleware] Error enviando a Replica2: {e}") 

        # Replica 3 
        try: 
            r3 = Pyro5.api.Proxy(REPLICA3_URI) 
            print(f"[Middleware] Enviando clave '{key}' -> '{value}' a Replica3") 
            resp3 = r3.write(key, value) 
            print(f"[Middleware] Respuesta de Replica3: {resp3}") 
            responses.append(resp3) 
            r3._pyroRelease() 
        except Exception as e: 
            responses.append(f"Error réplica3: {e}") 
            print(f"[Middleware] Error enviando a Replica3: {e}") 
 
        return responses 
 
    @Pyro5.api.expose 
    def read(self, key): 
        # Intentar leer de la réplica1, si falla usar réplica2 
        try: 
            r1 = Pyro5.api.Proxy(REPLICA1_URI) 
            val = r1.read(key) 
            r1._pyroRelease() 
            print(f"[Middleware] Lectura clave '{key}' desde Replica1 -> {val}") 
            return val 
        except: 
            try: 
                r2 = Pyro5.api.Proxy(REPLICA2_URI) 
                val = r2.read(key) 
                r2._pyroRelease() 
                print(f"[Middleware] Lectura clave '{key}' desde Replica2 -> {val}") 
                return val 
            except:
                try: 
                    r3 = Pyro5.api.Proxy(REPLICA3_URI) 
                    val = r3.read(key) 
                    r3._pyroRelease() 
                    print(f"[Middleware] Lectura clave '{key}' desde Replica3 -> {val}") 
                    return val
                except Exception as e: 
                    print(f"[Middleware] Error leyendo clave '{key}': {e}") 
                    return f"Error al leer: {e}" 
 
if __name__ == "__main__": 
    mw = Middleware() 
    daemon = Pyro5.api.Daemon(host=PYRO_HOST, port=PYRO_PORT) 
    uri = daemon.register(mw, objectId="middleware") 
    print(f"Middleware listo en: {uri}") 
    daemon.requestLoop() 