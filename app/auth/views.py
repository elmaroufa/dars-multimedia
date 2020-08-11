from flask import render_template,redirect,url_for,request,flash
from . import auth
from flask_login import login_user,login_required,logout_user
from .form import LoginForm, RegisterForm, PrediForm
from ..models import User, Predicateur, Multimedia, Newsletter
from app import db

'''
fonction add request form predicateur
'''
def idratePredicateur(predicateur):
    predicateur.name = request.form['name_predi']
    predicateur.language = request.form['language_predi']
    predicateur.descriptions = request.form['descr_predi']
    predicateur.city = request.form['city_predi']
    predicateur.info_youtube = request.form['youtube_predi']
    predicateur.info_telegram = request.form['telegram_predi']
    predicateur.author_id = request.form['user_id']
    return predicateur

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

'''
list all predicateur for media
'''
@auth.route('/all_predicateur')
@login_required
def all_predicateur():
        predicateurs = Predicateur.query.all()
        return render_template('main.vue_predicateur',predicateurs=predicateurs)


@auth.route('/add_predicateur',methods=['POST','GET'])
@login_required
def add_predicateur():
    predicateur = Predicateur()
    if request.method == 'POST':
        predi = idratePredicateur(predicateur)
        db.session.add(predi)
        db.session.commit()
        flash('Creation de predicateur reussi', 'success')
    return render_template('add_predicateur.html')



@auth.route('/admin/predicateur/update/<int:predi_id>',methods=['POST','GET'])
@login_required
def update_predicateur(predi_id):
    predicateur = Predicateur.query.get_or_404(predi_id)
    formpredi = PrediForm()
    if request.method == 'POST':
        predicateur = idratePredicateur(predicateur)
        db.session.commit()
        flash('Modificateur terminer','success')
        return redirect(url_for('auth.all_predicateur'))
    return render_template('update_predi.html',predicateur=predicateur,formpredi=formpredi)

'''
delete predicateur
'''
@auth.route('/admin/predicateur/delete/<int:predi_id>')
@login_required
def delete_predi(predi_id):
    predicateur = Predicateur.query.get_or_404(predi_id)
    media = Multimedia.query.filter_by(predicateur_id=predi_id)
    db.session.delete(predicateur)
    db.session.delete(media)
    db.session.commit()
    flash('supression predicateur reussi','succes')
    return redirect(url_for('auth.all_predicateur'))









