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
    last_course = Multimedia.query.filter_by(type_course='COURSE').all()
    last_simpleMedia = Multimedia.query.filter_by(index_media=0).all()
    last_simpleMedia.reverse()
    last_course.reverse()
    total_course = last_course
    total_media = last_simpleMedia
    nombre_course = len(last_course)
    nombre_media = len(total_media)
    if nombre_course > 2:
        total_course = indexLastMedia(total_course)
    return render_template('main.html',courses=total_course)
        
        

    return render_template('home.html')