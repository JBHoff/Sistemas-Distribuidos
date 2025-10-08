# Objetivo: 
Implementar un sistema distribuido donde vehículos reporten su posición GPS 
periódicamente y un servidor central los asigne a clientes según proximidad. 
---
1.  Conceptos previos: Posicionamiento Global (GPS) 
* El GPS permite determinar latitud y longitud de vehículos y clientes. 
* Se usa para calcular la distancia real entre vehículo y cliente usando geopy. 
* Latitud y longitud se representan como: 
* Latitud: 19.4340  (ej. Ciudad de México) 
* Longitud: -99.1320 
---
2. Requisitos de Software 
* Python 3.10+ 
* Pyro5 → middleware de comunicación remota 
* geopy → cálculo de distancias 
* Editor de texto (VSCode, PyCharm, etc.) 
* Terminal / CMD / PowerShell
---
3. Instalación de dependencias 
* python -m venv venv 
* source venv/bin/activate   `Linux/Mac` 
* venv\Scripts\activate `Windows` 
* pip install Pyro5 geopy 
python -c "import Pyro5; import geopy; print('Instalación correcta')" 
---
4. Archivos del proyecto 
proyecto_uber_distribuido/ 
│ 
├── servidor.py 
├── vehiculo.py 
├── cliente.py 
├── utils.py 
└── README.md
---
6. Salida visual esperada 
---
a) Consola del servidor 
 Servidor central iniciado 
 Servidor registrado en Name Server como 'servidor.central' 
 Vehículo V1 registrado en (19.4340, -99.1320) [Disponible] 
 Vehículo V2 registrado en (19.4335, -99.1325) [Disponible] 
 
 Vehículos registrados: {'V1': {'lat': 19.4340, 'lon': -99.1320, 'ocupado': False}, 
                           'V2': {'lat': 19.4335, 'lon': -99.1325, 'ocupado': False}} 
 Vehículo V1 asignado (distancia 0.05 km) 
Vehículo V1 liberado 
---
b) Consola del vehículo 
 ID del vehículo: V1 
 Ingresa tu latitud (ej. 19.4340): 19.4340 
 Ingresa tu longitud (ej. -99.1320): -99.1320 
 V1 activo. Enviando coordenadas... 
---
c) Consola del cliente 
 Ingresa tu latitud (ej. 19.4340): 19.4341 
 Ingresa tu longitud (ej. -99.1321): -99.1321 
 ID del cliente: C001 
 Solicitando vehículo cercano... 
 Vehículo asignado: V1 
 Tiempo de respuesta: 0.0032 s 
 Presiona ENTER cuando finalice el viaje... 
 Vehículo V1 liberado. Gracias por usar el servicio.
---