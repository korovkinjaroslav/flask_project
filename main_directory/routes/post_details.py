import requests
from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user

from main_directory.forms.commentForms import CommentForm
from main_directory.models.data import db_session
from main_directory.models.data.posts import Post
from main_directory.models.data.comments import Comment
from main_directory.models.data.users import User

detail_router = Blueprint("detail_router", __name__)


def _get_post_json(post_id):
    r = requests.get(f"http://127.0.0.1:5000/api/posts/{post_id}")
    if r.status_code != 200:
        return None
    data = r.json()
    return data.get("post")


def _load_comments(post_id):
    sess = db_session.create_session()
    out = []
    for c in sess.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at).all():
        u = sess.get(User, c.user_id)
        out.append({
            "content": c.content,
            "author": u.username if u else "?",
            "created_at": c.created_at,
            "user_id": u.id,
            "id": c.id
        })
    return out


@detail_router.route("/details/<int:post_id>")
def show_post(post_id):
    post = _get_post_json(post_id)
    if post is None:
        return redirect("/")
    comments = _load_comments(post_id)
    form = CommentForm()
    if session.get("_user_id") == None:
        is_admin = False
    else:
        is_admin = db_session.create_session().get(User, session.get('_user_id')).status
    return render_template(
        "post_details.html",
        title="Пост",
        post=post,
        comments=comments,
        form=form,
        is_admin=is_admin,
    )


@detail_router.route("/details/<int:post_id>/add_comment", methods=["POST"])
@login_required
def add_comment(post_id):
    form = CommentForm()
    sess = db_session.create_session()
    if sess.get(Post, post_id) is None:
        return redirect("/")
    if form.validate_on_submit():
        com = Comment(
            content=form.content.data.strip(),
            user_id=current_user.id,
            post_id=post_id,
        )
        sess.add(com)
        sess.commit()
        return redirect(url_for("detail_router.show_post", post_id=post_id))
    post = _get_post_json(post_id)
    if post is None:
        return redirect("/")
    comments = _load_comments(post_id)
    if session.get("_user_id") == None:
        is_admin = False
    else:
        is_admin = db_session.create_session().get(User, session.get('_user_id')).status
    return render_template(
        "post_details.html",
        title="Пост",
        post=post,
        comments=comments,
        form=form,
        is_admin=is_admin
    )
