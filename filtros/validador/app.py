from flask import Flask, request, jsonify
import re

app = Flask(__name__)
CAMPOS_REQUERIDOS = ["cedula", "nombre", "apellido", "edad", "telefono"]

@app.route("/filtros/validar", methods=["POST"])
def validar():
    contexto = request.get_json()
    
    # Verificar campos requeridos
    campos_faltantes = [c for c in CAMPOS_REQUERIDOS if not contexto.get(c)]
    if campos_faltantes:
        return jsonify({
            "estado": "error",
            "mensaje": f"Faltan campos: {campos_faltantes}"
        }), 400
    
    cedula = str(contexto.get("cedula", ""))
    if not cedula.isdigit() or len(cedula) != 10:
        return jsonify({
            "estado": "error",
            "mensaje": "Cedula debe tener 10 digitos"
        }), 400
    
    edad = contexto.get("edad")
    if not isinstance(edad, int) or not (0 <= edad <= 120):
        return jsonify({
            "estado": "error",
            "mensaje": "Edad debe ser entero entre 0 y 120"
        }), 400
    
    telefono = str(contexto.get("telefono", ""))
    if not telefono.isdigit() or not (7 <= len(telefono) <= 15):
        return jsonify({
            "estado": "error",
            "mensaje": "Telefono debe tener 7-15 digitos"
        }), 400
    
    email = contexto.get("email")
    if email:  # Solo validar si está presente
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return jsonify({
                "estado": "error",
                "mensaje": "Ingrese un email valido"
            }), 400
    
    return jsonify({
        "estado": "ok",
        "mensaje": "Datos validos",
        "datos": {"datos_validados": True}
    }), 200

if __name__ == "__main__":
    app.run(port=5002, debug=True)
