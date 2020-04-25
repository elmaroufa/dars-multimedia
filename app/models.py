from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(UserMixin,db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique= True)
    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique= True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash= db.Column(db.String(128))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def very_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username
    

class Multimedia(db.Model):
    __tablename__ = 'multimedias'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70),index=True)
    type_media = db.Column(db.String(64),nullable=True)
    theme = db.Column(db.String(64),nullable=True)
    body_iframe = db.Column(db.Text)
    link_dowload = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_difusion = db.Column(db.DateTime,nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    predicateur_id = db.Column(db.Integer, db.ForeignKey('predicateurs.id'))

    def __repr__(self):
        return '<Multimedia %r>' % self.title


class Predicateur(db.Model):
    __tablename__ = 'predicateurs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70),index=True)
    language = db.Column(db.String(64),nullable=True)
    descriptions = db.Column(db.Text)
    city = db.Column(db.String(64),nullable=True)
    info_youtube = db.Column(db.String(100),nullable=True)
    info_telegram = db.Column(db.String(100),nullable=True)
    preches = db.relationship('Multimedia', backref='predicateur', lazy='dynamic')
    

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    is_read = db.Column(db.Boolean,default=False)
