from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import database as db

app = Flask(__name__)


MENSAJES_MOTIVACIONALES = [
    "Hoy tienes una nueva oportunidad para avanzar. ☀️",
    "Un pequeño paso hoy mantiene tu impulso. 🔥",
    "¡Ya empezaste! Sigue construyendo tu racha. 💪",
    "Tu constancia está dando resultados. 🚀",
]


@app.route("/")
def index():
    habitos = db.obtener_habitos()

    habitos_con_datos = []
    for habito in habitos:
        racha = db.calcular_racha(habito["id"])
        ultimos_7_dias = db.obtener_ultimos_7_dias(habito["id"])
        habitos_con_datos.append({
            **habito,
            "racha": racha,
            "ultimos_7_dias": ultimos_7_dias
        })

    mensaje = random.choice(MENSAJES_MOTIVACIONALES)

    return render_template(
        "index.html",
        habitos=habitos_con_datos,
        mensaje=mensaje
    )


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo_habito():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if nombre:
            db.crear_habito(nombre, descripcion)

        return redirect(url_for("index"))

    return render_template("nuevo_habito.html")


@app.route("/completar/<int:habito_id>", methods=["POST"])
def completar_habito(habito_id):
    exito = db.marcar_habito_hoy(habito_id)
    racha_actualizada = db.calcular_racha(habito_id)

    return jsonify({
        "exito": exito,
        "racha": racha_actualizada
    })


@app.route("/eliminar/<int:habito_id>", methods=["POST"])
def eliminar_habito(habito_id):
    db.eliminar_habito(habito_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)