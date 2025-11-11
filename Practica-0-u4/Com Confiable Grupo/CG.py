import time,random

nodos=["A", "B", "C", "D", "E","F","G","H","I","J","K","L"]
replicas={}

def env_grp(msg):
    for nodo in nodos:
        if random.random()>0.2:
            print(f"{nodo} no recibio el mensaje: {msg}")
        else:
            replicas[nodo]=msg
            print(f"{nodo} recibio el mensaje: {msg}")

env_grp("Actualizacion de inventario")
print("\n Estado de replicacion: ",replicas)