import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from flask import Flask, request, jsonify
from db.db import obtener_conexion

app = Flask(__name__)

@app.route("/filtros/registrar", methods=["POST"])
def registrar():
    ctx      = request.get_json()
    cedula   = ctx.get("cedula")
    nombre   = ctx.get("nombre")
    apellido = ctx.get("apellido")
    edad     = ctx.get("edad")
    telefono = ctx.get("telefono")
    email    = ctx.get("email", None)
    try:
        conn   = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM pacientes WHERE cedula = %s", (cedula,))
        if cursor.fetchone():
            cursor.close(); conn.close()
            return jsonify({"estado": "error",
                            "mensaje": f"Cedula {cedula} ya registrada"}), 400
        cursor.execute(
            """INSERT INTO pacientes
               (cedula, nombre, apellido, edad, telefono, email)
               VALUES (%s,%s,%s,%s,%s,%s)
               RETURNING id, fecha_registro""",
            (cedula, nombre, apellido, edad, telefono, email))
        fila = cursor.fetchone()
        conn.commit(); cursor.close(); conn.close()
    except Exception as e:
        return jsonify({"estado": "error", "mensaje": str(e)}), 500
    return jsonify({"estado": "ok",
                    "mensaje": f"Paciente {nombre} {apellido} registrado",
                    "datos": {"paciente_id": fila["id"],
                              "fecha_registro": str(fila["fecha_registro"])}}), 200

@app.route("/pacientes", methods=["GET"])
def listar():
    conn = obtener_conexion()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM pacientes ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify({"pacientes": rows, "total": len(rows)}), 200

if __name__ == "__main__":
    app.run(port=5003, debug=True)
