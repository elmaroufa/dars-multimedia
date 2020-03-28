from flask import render_template,redirect,url_for,request,flash
from . import auth
from flask_login import login_user,login_required,logout_user
from .form import LoginForm,RegisterForm
from ..models import User

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.very_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash("Invalid username or password",'danger')
    return render_template('auth/login.html',form=form)

@auth.route('/register')
def register():
    form = RegisterForm()
    return render_template('auth/register.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("user is logout")
    return redirect(url_for('main.index'))

