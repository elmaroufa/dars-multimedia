from flask_wtf import FlaskForm
from ..models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Email,Regexp,EqualTo

class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField('Username', validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username have only letter no special carater')])
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('password2',message='password much match.')])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
         if User.query.filter_by(email=field.data).first():
             raise ValidationError("email alredy register")

    def validate_username(self,field):
        if User.query.filter_by(username=field.data):
            raise ValidationError('user already using')

class PrediForm(FlaskForm):
    name = StringField('Nom Predicateur', validators=[DataRequired(), Length(min=1, max=64)])
    language = StringField('Langue predication', validators=[DataRequired(), Length(min=1, max=64)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=64)])
    city = StringField('Ville du predicateur', validators=[DataRequired(), Length(min=1, max=64)])
    info_youtube = StringField('Lien sur youtube', validators=[DataRequired(), Length(min=1, max=64)])
    info_telegram = StringField('Lien telegram', validators=[DataRequired(), Length(min=1, max=64)])


class MultimediForm(FlaskForm):
    title = StringField('Titre du media', validators=[DataRequired(), Length(min=1, max=64)])
    type_media = StringField('Type media', validators=[DataRequired(), Length(min=1, max=64)])
    theme = StringField('Theme du media', validators=[DataRequired(), Length(min=1, max=64)])
    body_iframe= TextAreaField('Html du media', validators=[DataRequired(), Length(min=1, max=500)])
    link_dowload = TextAreaField('Telechargement du media', validators=[DataRequired(), Length(min=1, max=500)])


class NewsletterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=1, max=64), Email()])