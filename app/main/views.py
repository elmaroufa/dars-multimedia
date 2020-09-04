from datetime import datetime
from flask import Flask, render_template,url_for,session,redirect
from ..models import User, Predicateur, Multimedia, Newsletter
from . import main
from .. import db


'''
fonction pour renvoyer uniquement les 3 derniers medias
'''
def indexLastMedia(lastmedia):
    i=0
    list_course = []
    while i<3:
        list_course.append(lastmedia[i])
        i = i+1
    return list_course


@main.route('/')
def index():
    last_course = Multimedia.query.filter_by(type_media='COURSES').all()
    lastSermont = Multimedia.query.filter_by(type_media='SERMONT VENDREDI').all()
    lastConference = Multimedia.query.filter_by(type_media='CONFERENCE').all()
    predicateurs = Predicateur.query.all()
    lastSermont.reverse()
    lastConference.reverse()
    last_course.reverse()
    return render_template('main.html',last_course=last_course,predicateurs=predicateurs, \
        lastConference=lastConference,lastSermont = lastSermont)


@main.route('/medias/<string:type_media>')
def allMedias(type_media):
    medias = Multimedia.query.filter_by(type_media=type_media).all()
    medias.reverse()
    return render_template('medias.html',medias=medias)
