from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from forms import CommentForm, LikeForm, PostForm
from models import Comment, Post, db


feed_bp = Blueprint("feed", __name__)

POSTS_PER_PAGE = 5
COMMENTS_PER_PAGE = 3


def _build_feed_context(post_form: PostForm | None = None):
    page = request.args.get("page", 1, type=int)
    pagination = db.paginate(
        select(Post).order_by(Post.created_at.desc()),
        page=page,
        per_page=POSTS_PER_PAGE,
        error_out=False,
    )
    posts = pagination.items
    comment_pages = {}

    for post in posts:
        cpage_key = f"cpage_{post.id}"
        cpage = request.args.get(cpage_key, 1, type=int)
        comment_pages[post.id] = db.paginate(
            select(Comment)
            .where(Comment.post_id == post.id)
            .order_by(Comment.created_at.desc()),
            page=cpage,
            per_page=COMMENTS_PER_PAGE,
            error_out=False,
        )

    return {
        "post_form": post_form or PostForm(),
        "comment_form": CommentForm(),
        "like_form": LikeForm(),
        "posts": posts,
        "pagination": pagination,
        "comment_pages": comment_pages,
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
        return redirect(request.referrer or url_for("feed.index"))

    return render_template("index.html", **_build_feed_context(form)), 400


@feed_bp.post("/posts/<int:post_id>/delete")
@login_required
def delete_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    if post.user_id != current_user.id:
        return redirect(request.referrer or url_for("feed.index"))

    db.session.delete(post)
    db.session.commit()
    return redirect(request.referrer or url_for("feed.index"))
