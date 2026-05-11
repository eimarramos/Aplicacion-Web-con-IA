from flask import Blueprint, abort, redirect, request, url_for
from flask_login import current_user, login_required

from forms import CommentForm, LikeForm
from models import Comment, Like, Post, db


social_bp = Blueprint("social", __name__)


@social_bp.post("/posts/<int:post_id>/like")
@login_required
def toggle_like(post_id: int):
    form = LikeForm()
    if not form.validate_on_submit():
        return redirect(request.referrer or url_for("feed.index"))

    post = db.get_or_404(Post, post_id)
    existing = Like.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if existing:
        db.session.delete(existing)
    else:
        db.session.add(Like(post_id=post.id, user_id=current_user.id))

    db.session.commit()
    return redirect(request.referrer or url_for("feed.index"))


@social_bp.post("/posts/<int:post_id>/comments")
@login_required
def create_comment(post_id: int):
    form = CommentForm()
    post = db.get_or_404(Post, post_id)

    if form.validate_on_submit():
        comment = Comment(text=form.text.data.strip(), post_id=post.id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()

    return redirect(request.referrer or url_for("feed.index"))


@social_bp.post("/comments/<int:comment_id>/delete")
@login_required
def delete_comment(comment_id: int):
    form = LikeForm()
    if not form.validate_on_submit():
        return redirect(request.referrer or url_for("feed.index"))

    comment = db.get_or_404(Comment, comment_id)

    if comment.user_id != current_user.id and comment.post.user_id != current_user.id:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer or url_for("feed.index"))
