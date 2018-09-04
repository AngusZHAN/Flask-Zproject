from app import app, db
from .forms import RegisterForm, LoginForm, PostForm
from .models import User, Post
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/')
@app.route('/index/')
def index():
    context = {
        'posts': Post.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username = form.username.data, 
                    telephone = form.telephone.data,       
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册完成，你现在可以登录了')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

    

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user, form.remember_me.data)
            return redirect(url_for('index'))
        flash('用户名或密码错误')
    return render_template('login.html', form = form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('index'))

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user = user)


@app.route('/publish/', methods = ['GET', 'POST'])
def publish():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title = form.title.data,
                    body = form.body.data,
                    author = current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('发布成功')
        return redirect(url_for('index'))
    return render_template('publish.html', form = form)

@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@app.route('/detail/<post_id>')
def detail(post_id):
    post_model = Post.query.filter(Post.id == post_id).first()
    return render_template('detail.html', post = post_model)

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(404)
    form = PostForm()
    if request.method == 'POST' and form.validate():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('文章修改成功')
        return redirect(url_for('post', id = post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form = form)