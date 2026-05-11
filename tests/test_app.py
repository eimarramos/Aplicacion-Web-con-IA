from app import create_app
from models import Comment, Like, Post, User, db


def build_app():
    return create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )


def create_user(email: str, username: str, password: str = "password123") -> User:
    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email: str, password: str = "password123"):
    return client.post(
        "/login",
        data={"email": email, "password": password, "remember_me": "y"},
        follow_redirects=True,
    )


def test_crear_publicacion_valida():
    app = build_app()
    client = app.test_client()

    with app.app_context():
        user = create_user("test1@example.com", "test_user_1")
        user_email = user.email
        user_id = user.id

    login(client, user_email)

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
        assert post.user_id == user_id


def test_validacion_sin_texto():
    app = build_app()
    client = app.test_client()

    with app.app_context():
        user = create_user("test2@example.com", "test_user_2")
        user_email = user.email

    login(client, user_email)

    response = client.post("/posts", data={"text": "", "image_url": ""})

    assert response.status_code == 400
    assert b"obligatorio" in response.data


def test_feed_muestra_publicaciones():
    app = build_app()

    with app.app_context():
        user = create_user("test3@example.com", "test_user_3")
        db.session.add(Post(text="Primera", image_url=None, user_id=user.id))
        db.session.add(Post(text="Segunda", image_url=None, user_id=user.id))
        db.session.commit()

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Primera" in response.data
    assert b"Segunda" in response.data


def test_eliminar_publicacion():
    app = build_app()
    client = app.test_client()

    with app.app_context():
        user = create_user("test4@example.com", "test_user_4")
        post = Post(text="A borrar", image_url=None, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        post_id = post.id
        email = user.email

    login(client, email)

    response = client.post(f"/posts/{post_id}/delete", follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Post, post_id) is None


def test_register_y_login():
    app = build_app()
    client = app.test_client()

    register_response = client.post(
        "/register",
        data={
            "username": "nuevo_usuario",
            "email": "nuevo@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )

    assert register_response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="nuevo@example.com").first()
        assert user is not None

    client.get("/logout", follow_redirects=True)
    login_response = login(client, "nuevo@example.com")
    assert login_response.status_code == 200


def test_like_toggle():
    app = build_app()
    client = app.test_client()

    with app.app_context():
        user = create_user("test5@example.com", "test_user_5")
        post = Post(text="Like me", image_url=None, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        post_id = post.id
        email = user.email
        user_id = user.id

    login(client, email)

    first = client.post(f"/posts/{post_id}/like", data={}, follow_redirects=True)
    assert first.status_code == 200

    with app.app_context():
        assert Like.query.filter_by(post_id=post_id, user_id=user_id).count() == 1

    second = client.post(f"/posts/{post_id}/like", data={}, follow_redirects=True)
    assert second.status_code == 200

    with app.app_context():
        assert Like.query.filter_by(post_id=post_id, user_id=user_id).count() == 0


def test_comentario_y_permiso_de_eliminacion():
    app = build_app()
    client_owner = app.test_client()
    client_other = app.test_client()

    with app.app_context():
        owner = create_user("owner@example.com", "owner")
        other = create_user("other@example.com", "other")
        post = Post(text="Con comentarios", image_url=None, user_id=owner.id)
        db.session.add(post)
        db.session.commit()
        post_id = post.id
        owner_id = owner.id

    login(client_owner, "owner@example.com")
    comment_resp = client_owner.post(
        f"/posts/{post_id}/comments",
        data={"text": "Primer comentario"},
        follow_redirects=True,
    )
    assert comment_resp.status_code == 200

    with app.app_context():
        comment = Comment.query.filter_by(post_id=post_id, user_id=owner_id).first()
        assert comment is not None
        comment_id = comment.id

    login(client_other, "other@example.com")
    forbidden = client_other.post(
        f"/comments/{comment_id}/delete",
        data={},
        follow_redirects=False,
    )
    assert forbidden.status_code == 403

    owner_delete = client_owner.post(
        f"/comments/{comment_id}/delete",
        data={},
        follow_redirects=True,
    )
    assert owner_delete.status_code == 200

    with app.app_context():
        assert db.session.get(Comment, comment_id) is None
