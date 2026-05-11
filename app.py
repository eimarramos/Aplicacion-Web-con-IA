from flask import Flask, flash, redirect, render_template, url_for

from config import Config
from forms import PostForm
from models import Post, db


def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.get("/")
    def index() -> str:
        form = PostForm()
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("index.html", form=form, posts=posts)

    @app.post("/posts")
    def create_post():
        form = PostForm()
        if form.validate_on_submit():
            image_url = (form.image_url.data or "").strip() or None
            post = Post(text=form.text.data.strip(), image_url=image_url)
            db.session.add(post)
            db.session.commit()
            flash("Publicacion creada.", "success")
            return redirect(url_for("index"))

        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("index.html", form=form, posts=posts), 400

    @app.post("/posts/<int:post_id>/delete")
    def delete_post(post_id: int):
        post = db.get_or_404(Post, post_id)
        db.session.delete(post)
        db.session.commit()
        flash("Publicacion eliminada.", "success")
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
