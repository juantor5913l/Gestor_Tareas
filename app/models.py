from app import db
from datetime import datetime

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    prioridad = db.Column(db.String(20), default="Media")
    estado = db.Column(db.String(50), default="Pendiente")

    fecha_limite = db.Column(db.Date, nullable=False)
    creada = db.Column(db.DateTime, default=datetime.utcnow)
    actualizada = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)