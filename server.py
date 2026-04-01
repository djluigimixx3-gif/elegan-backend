from flask import Flask, request, jsonify
from flask_cors import CORS # Importa CORS
import os # Importamos os para obtener el puerto de las variables de entorno

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
        # Imprime esto en la consola de Render para depuración
        print("Error: Request no es JSON")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.json

    # Validamos la estructura mínima que esperamos de MTA
    if data and "online" in data and "playersCount" in data and "players" in data:
        data_store = data # Guardamos directamente el objeto recibido
        print(f"Datos recibidos y actualizados: {data_store}") # Para depuración en tu consola del backend de Render
        return jsonify({"status": "ok", "message": "Data updated"})
    else:
        print(f"Datos inválidos recibidos: {data}") # Para depuración
        return jsonify({"status": "error", "message": "Invalid data format"}), 400

@app.route("/api/status", methods=["GET"])
def status():
    # El frontend espera una LISTA que contenga nuestro objeto de estado.
    # Así que, envolvemos data_store en una lista.
    # Print para depuración, ver qué se envía al frontend
    print(f"Enviando estado al frontend: {[data_store]}")
    return jsonify([data_store])

# NOTA: Eliminamos app.run() para producción en Render.
# Render usará el start command con Waitress para iniciarlo.
# El if __name__ == '__main__': es para pruebas locales, pero no se ejecutará en Render.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) # Usa el puerto de Render si existe, sino 5000
    app.run(debug=True, host='0.0.0.0', port=port)
