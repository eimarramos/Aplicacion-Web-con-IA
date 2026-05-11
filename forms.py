from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL, ValidationError

from models import User


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
        validators=[Optional(), URL(message="Ingresa una URL valida.")],
    )


class RegisterForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[
            DataRequired(message="El usuario es obligatorio."),
            Length(min=3, max=20, message="El usuario debe tener entre 3 y 20 caracteres."),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio."),
            Email(message="Ingresa un email valido."),
        ],
    )
    password = PasswordField(
        "Contrasena",
        validators=[
            DataRequired(message="La contrasena es obligatoria."),
            Length(min=8, message="La contrasena debe tener al menos 8 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar contrasena",
        validators=[
            DataRequired(message="Confirma tu contrasena."),
            EqualTo("password", message="Las contrasenas no coinciden."),
        ],
    )
    submit = SubmitField("Crear cuenta")

    def validate_username(self, field: StringField) -> None:
        existing = User.query.filter_by(username=field.data.strip()).first()
        if existing:
            raise ValidationError("Este usuario ya esta en uso.")

    def validate_email(self, field: StringField) -> None:
        existing = User.query.filter_by(email=field.data.strip().lower()).first()
        if existing:
            raise ValidationError("Este email ya esta registrado.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio."),
            Email(message="Ingresa un email valido."),
        ],
    )
    password = PasswordField(
        "Contrasena",
        validators=[DataRequired(message="La contrasena es obligatoria.")],
    )
    remember_me = BooleanField("Recordarme")
    submit = SubmitField("Iniciar sesion")


class CommentForm(FlaskForm):
    text = StringField(
        "Comentario",
        validators=[
            DataRequired(message="El comentario es obligatorio."),
            Length(max=300, message="El comentario no puede superar 300 caracteres."),
        ],
    )


class LikeForm(FlaskForm):
    pass


class ProfileForm(FlaskForm):
    display_name = StringField(
        "Nombre visible",
        validators=[
            DataRequired(message="El nombre visible es obligatorio."),
            Length(max=80, message="El nombre visible no puede superar 80 caracteres."),
        ],
    )
    bio = TextAreaField(
        "Bio",
        validators=[Optional(), Length(max=280, message="La bio no puede superar 280 caracteres.")],
    )
    avatar_url = StringField(
        "URL de avatar",
        validators=[Optional(), URL(message="Ingresa una URL valida para el avatar.")],
    )
    submit = SubmitField("Guardar perfil")
