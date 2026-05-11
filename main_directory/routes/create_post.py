import base64

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from main_directory.forms.userForms import CreatePostForm
from main_directory.models.data import db_session
from main_directory.models.data.posts import Post

create_post_router = Blueprint("create_post_router", __name__)


@create_post_router.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        image_dataurl = None
        f = form.image.data
        if f and getattr(f, 'filename', None):
            raw = f.read()
            name = f.filename.lower()
            if name.endswith('.png'):
                mime = 'image/png'
            else:
                mime = 'image/jpeg'
            b64 = base64.b64encode(raw).decode('ascii')
            image_dataurl = 'data:' + mime + ';base64,' + b64
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=image_dataurl,
            user_id=current_user.id,
            likes_amount=0,
        )
        sess.add(post)
        sess.commit()
        return redirect(f"/main_page/{post.id}")
    return render_template('create_post.html', title='Новый пост', form=form)
