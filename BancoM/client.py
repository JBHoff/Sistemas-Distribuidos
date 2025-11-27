# client.py
import Pyro5.api

middleware = Pyro5.api.Proxy("PYRO:middleware@192.168.1.20:4000")

print(middleware.login("123", "ClienteA"))
print(middleware.deposit("123", 100))
print(middleware.logout("123", "ClienteA"))
