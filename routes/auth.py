from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from forms import LoginForm, ProfileForm, RegisterForm
from models import User, db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("feed.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            display_name=form.username.data.strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Cuenta creada. Bienvenido.", "success")
        return redirect(url_for("feed.index"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("feed.index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Sesion iniciada.", "success")
            return redirect(url_for("feed.index"))

        flash("Credenciales invalidas.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesion cerrada.", "success")
    return redirect(url_for("feed.index"))


@auth_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm(
        display_name=current_user.display_name or current_user.username,
        bio=current_user.bio,
        avatar_url=current_user.avatar_url,
    )

    if form.validate_on_submit():
        current_user.display_name = form.display_name.data.strip()
        current_user.bio = (form.bio.data or "").strip() or None
        current_user.avatar_url = (form.avatar_url.data or "").strip() or None
        db.session.commit()
        flash("Perfil actualizado.", "success")
        return redirect(url_for("auth.edit_profile"))

    return render_template("auth/profile.html", form=form)
