from flask import Blueprint, request, render_template, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import re
import datetime
from sqlalchemy.exc import IntegrityError

from .helpers import *
from .models import *
from . import db

from . import countries

search = Blueprint('search', __name__)

@login_required
@search.route('/search/driver', methods = ['GET', 'POST'])
def search_drivers():
    season = datetime.datetime.now().year
    
    drivers = db.session.execute(
        db.select(Driver.driver_id, Driver.first_name, Driver.last_name, Driver.driver_num, Driver.nationality)
        .join(DriverStanding, DriverStanding.driver_id == Driver.driver_id)
        .filter(DriverStanding.season == season)
    ).all()
    
    drivers_list = []
    for driver in drivers:
        name = ' '.join([driver.first_name, driver.last_name])
        
        for country in countries:
            if country['demonyms']['eng']['f'] == driver.nationality:
                driver_country = country['cca2'].upper()
        
        driver_id = driver.driver_id
        if driver.driver_id.find(' ') != -1:
            driver_id = driver.driver_id.replace(' ', '')
        
        driver_img = f"/static/drivers/{driver_id}.jpg"    
        flag_url = f"http://purecatamphetamine.github.io/country-flag-icons/3x2/{driver_country}.svg"
        
        number = driver.driver_num
        if driver.driver_id == 'max_verstappen':
            number = 1
        
        
        driver_dict = {
            'name': name,
            'id': driver.driver_id,
            'number': number,
            'driver_img': driver_img,
            'flag': flag_url
        }
        drivers_list.append(driver_dict)
    return render_template('search_driver.html', drivers=drivers_list, season = season)

@login_required
@search.route('/search/constructor', methods = ['GET', 'POST'])
def search_constructors():
    season = datetime.datetime.now().year
    
    constructors = db.session.execute(
        db.select(Constructor.constructor_id, Constructor.constructor_name, Constructor.nationality)
        .join(ConstructorStanding, ConstructorStanding.constructor_id == Constructor.constructor_id)
        .filter(ConstructorStanding.season == season)
    ).all()
    
    constructor_list = []
    for constructor in constructors:
        fav_team_url = constructor.constructor_id
    
        if fav_team_url == 'sauber':
            fav_team_url = 'kick sauber'
    
        if constructor.constructor_id.find('_') != -1:
            fav_team_url = constructor.constructor_id.replace('_', ' ')
        
        fav_team_url = fav_team_url.title()
    
        team_url = f"https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_475/content/dam/fom-website/2018-redesign-assets/team%20logos/{fav_team_url}"
        
        for country in countries:
            if country['demonyms']['eng']['f'] == constructor.nationality:
                con_country = country['cca2'].upper()
        
        flag_url = f"http://purecatamphetamine.github.io/country-flag-icons/3x2/{con_country}.svg"
        
        con_dict = {
            'name' : constructor.constructor_name,
            'id' : constructor.constructor_id,
            'flag' : flag_url,
            'team_img': team_url
        }
        constructor_list.append(con_dict)
    
    return render_template('search_constructor.html', constructors = constructor_list, season = season)