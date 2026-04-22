from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PIPELINE = [
    {"nombre": "Validador de datos",
     "url":    "http://localhost:5002/filtros/validar"},
    {"nombre": "Registrador en base de datos",
     "url":    "http://localhost:5003/filtros/registrar"},
]

@app.route("/pipeline/ejecutar", methods=["POST"])
def ejecutar_pipeline():
    contexto  = request.get_json()
    historial = []
    for filtro in PIPELINE:
        try:
            respuesta = requests.post(filtro["url"], json=contexto, timeout=10)
        except requests.exceptions.ConnectionError:
            return jsonify({"estado": "error",
                            "paso": filtro["nombre"],
                            "historial": historial}), 503
        resultado = respuesta.json()
        historial.append({"filtro": filtro["nombre"], "resultado": resultado})
        if resultado.get("estado") != "ok":
            return jsonify({"estado": "error",
                            "paso": filtro["nombre"],
                            "mensaje": resultado.get("mensaje"),
                            "historial": historial}), 400
        contexto.update(resultado.get("datos", {}))
    return jsonify({"estado": "ok",
                    "mensaje": "Paciente registrado correctamente",
                    "paciente_id": contexto.get("paciente_id"),
                    "historial": historial}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)

