from . import main
from .forms import PostForm, QuestionForm, AnswerForm
from .. import db
from ..models import User, Post, Question, Answer
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_required, login_user, logout_user, current_user

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
    return render_template('user.html', user = user)


@main.route('/publish/', methods = ['GET', 'POST'])
def publish():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title = form.title.data,
                    body = form.body.data,
                    author = current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('发布成功')
        return redirect(url_for('.index'))
    return render_template('publish.html', form = form)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@main.route('/detail/<post_id>')
def detail(post_id):
    post_model = Post.query.filter(Post.id == post_id).first()
    return render_template('detail.html', post = post_model)

@main.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        flash('您不是文章作者，无法修改。')
        return redirect(url_for('.index'))
    form = PostForm()
    if request.method == 'POST' and form.validate():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('文章修改成功')
        return redirect(url_for('.post', id = post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form = form)

@main.route('/question/', methods = ['GET', 'POST'])
def question():
    form = QuestionForm(request.form)
    if request.method == 'POST' and form.validate():
        question = Question(title = form.title.data,
                            body = form.body.data,
                            author = current_user._get_current_object())
        db.session.add(question)
        db.session.commit()
        flash('发布成功')
        return redirect(url_for('.index'))
    return render_template('question.html', form = form)

@main.route('/add_answer/', methods = ['GET', 'POST'])
def add_answer():
    form = AnswerForm()
    answer = Answer(body = form.body.data,
                    author = current_user._get_current_object())
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
    return render_template('detail.html', question = question_model)