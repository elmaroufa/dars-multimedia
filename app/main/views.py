from datetime import datetime
from flask import Flask, render_template,url_for,session,redirect
from . import main
from .. import db

@main.route('/')
def index():
    return render_template('home.html')