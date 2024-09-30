from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from os import path, listdir
from time import sleep
import fastf1
import random
import string
import datetime
import requests
import json

db = SQLAlchemy()
DB_NAME = "f1.db"

base_url = 'http://ergast.com/api/f1'

# scheduler = APScheduler(scheduler=BackgroundScheduler())
base_dir = path.dirname(path.abspath(__file__))
countries_file_path = path.join(base_dir, 'countries.json')
with open(countries_file_path, 'r') as file:
    countries = json.load(file)
    
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ''.join(random.choices(string.ascii_lowercase, k = 10)) #generate a random string of 10 characters
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize Session
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SCHEDULER_API_ENABLED'] = True
    Session(app)
    
    # tell database what app I'm using
    db.init_app(app) 
        
    from .views import views
    from .auth import auth
    from .standings import standings
    from .search import search
    from .news import news
    from .compare import compare
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(standings, url_prefix='/')
    app.register_blueprint(search, url_prefix='/')
    app.register_blueprint(news, url_prefix='/')
    app.register_blueprint(compare, url_prefix='/')
    
    #db models need to exist before database creation
    from .models import User, Driver, Constructor, Circuit, Race, Result, DriverConstructor, DriverStanding
    # from .models import Sessions
    
    with app.app_context():
        db.create_all()
        print('Created Database!')
    
    return app
            
