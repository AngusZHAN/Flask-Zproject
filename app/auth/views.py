from flask import render_template, redirect, session, flash, url_for, request
from . import auth
from .. import db
from ..models import User
from .forms import RegisterForm, LoginForm
from flask_login import login_required, login_user, logout_user, current_user

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username = form.username.data, 
                    telephone = form.telephone.data,       
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册完成，你现在可以登录了')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)

    

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('用户名或密码错误')
    return render_template('auth/login.html', form = form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('main.index'))