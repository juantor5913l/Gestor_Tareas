from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Tarea
from datetime import datetime, date

main = Blueprint("main", __name__)


@main.route("/")
def tablero():
    busqueda = request.args.get("q", "")

    query = Tarea.query

    if busqueda:
        query = query.filter(Tarea.titulo.contains(busqueda))

    tareas = query.order_by(Tarea.fecha_limite.asc()).all()

    pendientes = [t for t in tareas if t.estado == "Pendiente"]
    proceso = [t for t in tareas if t.estado == "En proceso"]
    completadas = [t for t in tareas if t.estado == "Completada"]

    return render_template(
        "tablero.html",
        pendientes=pendientes,
        proceso=proceso,
        completadas=completadas,
        today=date.today()
    )


@main.route("/hoy")
def hoy():
    hoy = date.today()

    tareas_hoy = Tarea.query.filter(
        Tarea.fecha_limite == hoy
    ).order_by(Tarea.fecha_limite.asc()).all()

    return render_template(
        "hoy.html",
        tareas=tareas_hoy
    )


@main.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()

        tarea = Tarea(
            titulo=request.form["titulo"],
            descripcion=request.form["descripcion"],
            prioridad=request.form["prioridad"],
            fecha_limite=fecha
        )

        db.session.add(tarea)
        db.session.commit()

        flash("Tarea creada correctamente")

        return redirect(url_for("main.tablero"))

    return render_template("crear_tarea.html")


@main.route("/estado/<int:id>/<nuevo>")
def cambiar_estado(id, nuevo):
    tarea = Tarea.query.get_or_404(id)

    tarea.estado = nuevo
    db.session.commit()

    flash("Estado actualizado")

    return redirect(url_for("main.tablero"))


@main.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    tarea = Tarea.query.get_or_404(id)

    if request.method == "POST":
        tarea.titulo = request.form["titulo"]
        tarea.descripcion = request.form["descripcion"]
        tarea.prioridad = request.form["prioridad"]
        tarea.fecha_limite = datetime.strptime(
            request.form["fecha"], "%Y-%m-%d"
        ).date()

        db.session.commit()

        flash("Tarea actualizada")

        return redirect(url_for("main.tablero"))

    return render_template("editar_tarea.html", tarea=tarea)


@main.route("/eliminar/<int:id>")
def eliminar(id):
    tarea = Tarea.query.get_or_404(id)

    db.session.delete(tarea)
    db.session.commit()

    flash("Tarea eliminada")

    return redirect(url_for("main.tablero"))


@main.route("/calendario")
def calendario():
    tareas = Tarea.query.all()

    eventos = []

    for tarea in tareas:
        eventos.append({
            "title": tarea.titulo,
            "start": tarea.fecha_limite.strftime("%Y-%m-%d"),
            "allDay": True,
            "color": "#ef4444" if tarea.prioridad == "Alta" else "#f59e0b" if tarea.prioridad == "Media" else "#22c55e"
        })

    return render_template("calendario.html", eventos=eventos)