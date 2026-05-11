from flask import Flask
from sqlalchemy import inspect, text

from config import Config
from extensions import login_manager
from models import User, db
from routes import auth_bp, feed_bp, social_bp


def _ensure_legacy_schema_compatibility() -> None:
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    if "user" in tables:
        user_columns = {column["name"] for column in inspector.get_columns("user")}

        if "display_name" not in user_columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN display_name VARCHAR(80)"))
            db.session.commit()

        if "bio" not in user_columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN bio VARCHAR(280)"))
            db.session.commit()

        if "avatar_url" not in user_columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN avatar_url VARCHAR(2048)"))
            db.session.commit()

        db.session.execute(text("UPDATE user SET display_name = username WHERE display_name IS NULL"))
        db.session.commit()

    if "post" not in tables:
        return

    post_columns = {column["name"] for column in inspector.get_columns("post")}
    if "user_id" in post_columns:
        return

    db.session.execute(text("ALTER TABLE post ADD COLUMN user_id INTEGER"))
    db.session.commit()

    legacy_user = User.query.filter_by(email="legacy@local").first()
    if legacy_user is None:
        username = "legacy_user"
        suffix = 1
        while User.query.filter_by(username=username).first() is not None:
            suffix += 1
            username = f"legacy_user_{suffix}"

        legacy_user = User(username=username, email="legacy@local")
        legacy_user.set_password("legacy-password")
        db.session.add(legacy_user)
        db.session.commit()

    db.session.execute(
        text("UPDATE post SET user_id = :user_id WHERE user_id IS NULL"),
        {"user_id": legacy_user.id},
    )
    db.session.commit()


def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()
        _ensure_legacy_schema_compatibility()

    app.register_blueprint(feed_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(social_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
