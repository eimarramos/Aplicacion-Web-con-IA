from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL


class PostForm(FlaskForm):
    text = TextAreaField(
        "Texto",
        validators=[
            DataRequired(message="El texto es obligatorio."),
            Length(max=500, message="El texto no puede superar 500 caracteres."),
        ],
    )
    image_url = StringField(
        "URL de imagen",
        validators=[
            Optional(),
            URL(message="Ingresa una URL valida.")
        ],
    )
