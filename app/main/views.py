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
    last_course.reverse()
    total_course = last_course
    nombre_course = len(last_course)
    if nombre_course > 2:
        new_course = []
        new_course.append(total_course[0])
        

    return render_template('home.html')