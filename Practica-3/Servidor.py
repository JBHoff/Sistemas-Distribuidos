from flask import Flask, request, jsonify 
from datetime import datetime 
app = Flask(__name__) 
# Lista para almacenar mensajes, con límite de 20 
MAX_MENSAJES = 20 
mensajes = [] 
# Ruta raíz opcional 
@app.route("/") 
def index(): 
    return "Servidor Flask del chat activo!" 
# Ruta para enviar mensaje 
@app.route("/enviar", methods=["POST"]) 
def enviar(): 
    data = request.get_json() 
    if not data or "mensaje" not in data or "usuario" not in data: 
        return jsonify({"error": "Falta 'mensaje' o 'usuario'"}), 400 
 
    mensaje = { 
        "usuario": data["usuario"], 
        "mensaje": data["mensaje"], 
        "hora": datetime.now().strftime("%H:%M:%S") 
    } 
 
    mensajes.append(mensaje) 
    # Mantener solo los últimos MAX_MENSAJES 
    if len(mensajes) > MAX_MENSAJES: 
        mensajes.pop(0) 
 
    print(f"[{mensaje['hora']}] {mensaje['usuario']}: {mensaje['mensaje']}") 
    return jsonify({"status": "ok", "servidor": f"Recibido: {mensaje['mensaje']}"}) 
 
# Ruta para recibir mensajes 
@app.route("/recibir", methods=["GET"]) 
def recibir(): 
    return jsonify(mensajes) 
 
if __name__ == "__main__": 
    app.run(host="192.168.1.53", port=5050, debug=True) 