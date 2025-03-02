from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId  # Importar ObjectId desde bson
import os

app = Flask(__name__)

# Conexión a MongoDB Atlas (la URI debe configurarse en las variables de entorno)
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["tareas_db"]
tareas = db["tareas"]

# Ruta para obtener todas las tareas
@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    tareas_lista = list(tareas.find())
    for tarea in tareas_lista:
        tarea["_id"] = str(tarea["_id"])  # Convertir ObjectId a string
    return jsonify(tareas_lista)

# Ruta para agregar una nueva tarea
@app.route("/tarea", methods=["POST"])
def agregar_tarea():
    titulo = request.json["titulo"]
    descripcion = request.json["descripcion"]
    fecha_vencimiento = request.json["fecha_vencimiento"]
    tarea = {
        "titulo": titulo,
        "descripcion": descripcion,
        "fecha_vencimiento": fecha_vencimiento,
        "estado": "pendiente"
    }
    tareas.insert_one(tarea)
    return jsonify({"message": "Tarea agregada correctamente!"}), 201

# Ruta para actualizar el estado de una tarea
@app.route("/tarea/<id_tarea>", methods=["PUT"])
def actualizar_tarea(id_tarea):
    nuevo_estado = request.json["estado"]
    tarea = tareas.find_one({"_id": ObjectId(id_tarea)})
    if tarea:
        tareas.update_one(
            {"_id": ObjectId(id_tarea)},
            {"$set": {"estado": nuevo_estado}}
        )
        return jsonify({"message": f"Tarea {id_tarea} actualizada a estado '{nuevo_estado}'."}), 200
    return jsonify({"message": "Tarea no encontrada."}), 404

# Ruta para eliminar una tarea
@app.route("/tarea/<id_tarea>", methods=["DELETE"])
def eliminar_tarea(id_tarea):
    tarea = tareas.find_one({"_id": ObjectId(id_tarea)})
    if tarea:
        tareas.delete_one({"_id": ObjectId(id_tarea)})
        return jsonify({"message": f"Tarea {id_tarea} eliminada."}), 200
    return jsonify({"message": "Tarea no encontrada."}), 404

if __name__ == "__main__":
    app.run(debug=True)
