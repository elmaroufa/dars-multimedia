from flask import render_template,redirect,url_for,request,flash
import string
import random
from datetime import datetime
from . import auth
from flask_login import login_user,login_required,logout_user
from .form import LoginForm, RegisterForm, PrediForm
from ..models import User, Predicateur, Multimedia, Newsletter
from app import db


'''
def return random string key by attribute code_course media
'''
def key_course():
    date_now = datetime.now()
    date_str = date_now.strftime("%d-%m-%Y")
    my_key = ''.join(random.choices(string.ascii_uppercase +  string.digits, k = 10))
    my_key = date_str + '-' + my_key
    return my_key

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

'''
test database table migrate
'''
@auth.route('/admin/test')
def test_marouf():
    mykey = key_course()
    return mykey


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

'''
add simple media
'''
@auth.route('/admin/media/add_simple_media',methods=['POST','GET'])
@login_required
def add_simple_media():
    media = Multimedia()
    predicateurs = Predicateur.query.all()
    media.title = request.form['title_media']
    media.type_media = request.form['type_media']
    media.theme = request.form['theme_media']
    if media.type_media == 'courses':
        media.index_media = 1
        media.code_course = key_course()
        media.course_descriptions = request.form['media_descriptions']
    else:
        media.index_media = 0
    media.body_iframe = request.form['iframe_media']
    media.link_dowload = request.form['link_media']
    media.date_difusion = request.form['difusion_date_media']
    media.author_id = request.form['autho_media']
    media.predicateur_id = request.form['predi_media']
    if request.method == 'POST':
        db.session.add(media)
        db.commit()
        flash('creation de media reussi','success')
    render_template("add_media_simple.html", predicateurs=predicateurs)


'''
add news cours media
'''
@auth.route('/admin/media/add_new_course/<int:id_first_media>',methods=['POST','GET'])
@login_required
def new_course(id_first_media):
    first_media = Multimedia.query.filter_by(id=id_first_media)


'''
views all media type conferences or sermont by predicateur
'''
@auth.route('/admin/predicateur/all_media/<int:predicateur_id>')
@login_required
def views_all_media(predicateur_id):
    media = Multimedia.query.filter_by(predicateur_id=predicateur_id,index_media=0).all()
    return media

'''
views all media courses
'''
@auth.route('/admin/predicateur/all_course/<int:predicateur_id>')
@login_required
def views_all_course(predicateur_id):
    media = Multimedia.query.filter_by(predicateur_id=predicateur_id,index_media=1).all()
    return media

'''
all chapitre courses
'''
@auth.route('/admin/predicateur/all_chapitre/<string:code_course')
@login_required
def all_chapitre(code_course):
    media = Multimedia.query.filter_by(code_course=code_course).all()
    return media

'''
add new chapitre course
'''
@auth.route('/admin/predicateur/new_chapitre', methods=['POST','GET'])
@login_required
def add_new_chapitre():
    code_course = request.form['code_course']
    mediaUpdate = Multimedia.query.filter_by(code_course=code_course).first()
    new_media = Multimedia()
    news_index  = Multimedia.query.filter_by(code_course=code_course).count()
    news_index = news_index + 1
    new_media.title = mediaUpdate.title
    new_media.type_media = mediaUpdate.type_media
    new_media.theme = mediaUpdate.theme
    new_media.code_course = code_course
    new_media.course_descriptions = request.form['course_descriptions']
    new_media.body_iframe = request.form['body_iframe']
    new_media.link_dowload = request.formm['link_dowload']
    new_media.author_id = request.form['id_author']
    new_media.predicateur_id = mediaUpdate.predicateur_id
    if request.method == 'POST':
        db.session.add(new_media)
        db.session.commit()
        flash('Ajout nouveau course reussi', 'success')
        return redirect(url_for('views_all_chapitre'))
    
    





