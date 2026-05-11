from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from forms import CommentForm, LikeForm, PostForm
from models import Post, db


feed_bp = Blueprint("feed", __name__)


def _build_feed_context(post_form: PostForm | None = None):
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return {
        "post_form": post_form or PostForm(),
        "comment_form": CommentForm(),
        "like_form": LikeForm(),
        "posts": posts,
    }


@feed_bp.get("/")
def index() -> str:
    return render_template("index.html", **_build_feed_context())


@feed_bp.post("/posts")
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image_url = (form.image_url.data or "").strip() or None
        post = Post(
            text=form.text.data.strip(),
            image_url=image_url,
            user_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("feed.index"))

    return render_template("index.html", **_build_feed_context(form)), 400


@feed_bp.post("/posts/<int:post_id>/delete")
@login_required
def delete_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    if post.user_id != current_user.id:
        return redirect(url_for("feed.index"))

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("feed.index"))
