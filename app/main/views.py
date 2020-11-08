from datetime import datetime
from flask import Flask, render_template,url_for,session,redirect
from ..models import User, Predicateur, Multimedia, Newsletter
from . import main
from .. import db


'''
fonction pour associer chaque media a un predicateur 
'''
def associatePredi(medias):
    i=0
    nombre = len(medias)
    while i < nombre:
        medias[i].predicateur = Predicateur.query.filter_by(id=medias[i].predicateur_id).first()
        i = i + 1

    

'''
controller home page
'''
@main.route('/')
def index():
    last_course = Multimedia.query.filter_by(type_media='COURSES').all()
    lastSermont = Multimedia.query.filter_by(type_media='SERMONT VENDREDI').all()
    lastConference = Multimedia.query.filter_by(type_media='CONFERENCE').all()
    predicateurs = Predicateur.query.all()
    lastSermont.reverse()
    lastConference.reverse()
    last_course.reverse()
    return render_template('main/main.html',last_course=last_course,predicateurs=predicateurs,\
        lastConference=lastConference,lastSermont = lastSermont)


'''
view all media in type
'''
@main.route('/medias/<string:type_media>')
def allMedias(type_media):
    medias = Multimedia.query.filter_by(type_media=type_media).all()
    associatePredi(medias)
    medias.reverse()
    return render_template('medias.html',medias=medias)

@main.route('/medias/course')
def allCourses():
    medias = Multimedia.query.filter_by(type_media='COURSES',index_media=1).all()
    associatePredi(medias)
    medias.reverse()
    return render_template('course.html',courses=medias)

@main.route('/medias/chapitre/<string:code_course>')
def allChapitre(code_course):
    medias = Multimedia.query.filter_by(code_course=code_course).all()
    associatePredi(medias)
    return render_template('chapitre.html',medias=medias)

@main.route('/medias/<int:id_media>')
def viewMedia(id_media):
    media = Multimedia.query.filter_by(id=id_media).first()
    predi = Predicateur.query.filter_by(id = media.predicateur_id).first()
    predicateur = predi.name
    return render_template('view_media.html',media=media,predicateur=predicateur)

@main.route('/predicateurs')
def allpredicateur():
    predicateur = Predicateur.query.all()
    return render_template('predicateur.html',predicateur=predicateur)

@main.route('/predicateur/media/<int:id_predicateur>')
def mediaPredicateur(id_predicateur):
    medias = Multimedia.query.filter_by(predicateur_id=id_predicateur,\
        index_media=0).all()
    courses = Multimedia.query.filter_by(predicateur_id = id_predicateur,\
        index_media=1).all()
    return render_template('media_predicateur',medias=medias,courses=courses)