from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(2048), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
