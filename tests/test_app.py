from app import create_app
from models import Post, db


def build_app():
    return create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )


def test_crear_publicacion_valida():
    app = build_app()
    client = app.test_client()

    response = client.post(
        "/posts",
        data={"text": "Hola desde pytest", "image_url": ""},
        follow_redirects=True,
    )

    assert response.status_code == 200
    with app.app_context():
        post = Post.query.first()
        assert post is not None
        assert post.text == "Hola desde pytest"


def test_validacion_sin_texto():
    app = build_app()
    client = app.test_client()

    response = client.post("/posts", data={"text": "", "image_url": ""})

    assert response.status_code == 400
    assert b"obligatorio" in response.data


def test_feed_muestra_publicaciones():
    app = build_app()

    with app.app_context():
        db.session.add(Post(text="Primera", image_url=None))
        db.session.add(Post(text="Segunda", image_url=None))
        db.session.commit()

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Primera" in response.data
    assert b"Segunda" in response.data


def test_eliminar_publicacion():
    app = build_app()

    with app.app_context():
        post = Post(text="A borrar", image_url=None)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    client = app.test_client()
    response = client.post(f"/posts/{post_id}/delete", follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Post, post_id) is None
