from flask import Flask, request, jsonify
from flask_cors import CORS # Importa CORS

app = Flask(__name__)
# Habilita CORS para todas las rutas y orígenes, esencial para peticiones de la web
CORS(app)

# Simplificamos data_store para que contenga directamente el objeto que quieres enviar
# Esto reflejará el ESTADO ACTUAL del servidor
data_store = {
    "online": False,
    "playersCount": 0,
    "players": []
}

@app.route("/")
def home():
    return "Backend funcionando"

@app.route("/api/update_players", methods=["POST"])
def update_players():
    global data_store

    # Asegúrate de que el body de la petición sea JSON
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.json

    # Validamos la estructura mínima que esperamos de MTA
    if data and "online" in data and "playersCount" in data and "players" in data:
        data_store = data # Guardamos directamente el objeto recibido
        print(f"Datos recibidos y actualizados: {data_store}") # Para depuración en tu consola del backend
        return jsonify({"status": "ok", "message": "Data updated"})
    else:
        print(f"Datos inválidos recibidos: {data}") # Para depuración
        return jsonify({"status": "error", "message": "Invalid data format"}), 400

@app.route("/api/status", methods=["GET"])
def status():
    # El frontend espera una LISTA que contenga nuestro objeto de estado.
    # Así que, envolvemos data_store en una lista.
    return jsonify([data_store])

if __name__ == '__main__':
    # Asegúrate de que este backend esté accesible públicamente si lo alojas en Render
    # o si tu MTA Server y tu web están en máquinas diferentes.
    # Si lo corres localmente para pruebas, 0.0.0.0 lo hace accesible desde otras máquinas en tu red.
    app.run(debug=True, host='0.0.0.0', port=5000) # O el puerto que uses en Render
