from . import main
from .. import db
from .forms import (
    PostForm,
    QuestionForm,
    AnswerForm,
    EditProfileForm,
)
from ..models import (
    User,
    Post,
    Question,
    Answer,
)
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session,
)
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)


@main.route('/')
@main.route('/index/')
def index():
    context = {
        'posts': Post.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    # posts = user.posts.order_by().all
    return render_template('user.html', user=user)


@main.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('修改资料成功')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/up_avatar/', methods=['GET', 'POST'])
@login_required
def up_avatar():
    avatar = request.files.get('file')
    fname = avatar.filename
    UPLOAD_FOLDER = "D:\\Code\\Flask-Zproject\\app\\static\\avatar\\"
    ALLOWED_EXTENSIONS = ['gif', 'png', 'jpg', 'jpeg']
    flag = '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    if not flag:
        flash('文件类型错误，请重试')
        return redirect(url_for('.user', username=current_user.username))
    avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, current_user.username, fname))
    current_user.i_avatar = '\\static\\avatar\\{}_{}'.format(current_user.username, fname)
    db.session.add(current_user)
    db.session.commit()
    flash('上传头像成功')
    return redirect(url_for('.user', username=current_user.username))


@main.route('/publish/', methods=['GET', 'POST'])
@login_required
def publish():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('发布成功')
        return redirect(url_for('.index'))
    return render_template('publish.html', form=form)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/detail/<post_id>')
def detail(post_id):
    post_model = Post.query.filter(Post.id == post_id).first()
    return render_template('detail.html', post=post_model)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        flash('您不是文章作者，无法修改。')
        return redirect(url_for('.index'))
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('文章修改成功')
        return redirect(url_for('.detail', post_id=Post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    form = QuestionForm(request.form)
    if request.method == 'POST' and form.validate():
        question = Question(title=form.title.data,
                            body=form.body.data,
                            author=current_user._get_current_object())
        db.session.add(question)
        db.session.commit()
        flash('发布成功')
        return redirect(url_for('.index'))
    return render_template('question.html', form=form)


@main.route('/add_answer/', methods=['GET', 'POST'])
@login_required
def add_answer():
    form = AnswerForm()
    answer = Answer(body=form.body.data,
                    author=current_user._get_current_object())
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    flash('回答成功')
    redirect(url_for('.q_detail', question_id=question_id))


@main.route('/q_detail/<question_id>')
def q_detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)
