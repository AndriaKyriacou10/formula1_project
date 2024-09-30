from flask import Blueprint, request, render_template, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import re
import datetime
import os
from sqlalchemy.exc import IntegrityError

from .helpers import *
from .models import *
from . import db

from . import countries

views = Blueprint('views', __name__)

@views.route('/')
def welcome_login():
    
    if ('user_id' in session):
        return redirect(url_for('views.home'))
    
    return render_template("welcome-login.html")

@login_required
@views.route('/home')
def home():
    user = User.query.filter_by(id = session['user_id']).first()

    driver = get_driver_data(user.fav_driver)
    driver_id = driver.driver_id
    last_name = driver.last_name
    number = driver.driver_num
   
    dob = [driver.dob.strftime('%d'), driver.dob.strftime('%m'), driver.dob.strftime('%Y')]
    dob = ' - '.join(dob)

    for country in countries:
        if country['demonyms']['eng']['f'] == driver.nationality:
            driver_country = country['cca2'].upper()
    
    results, driver_champ_count = get_driver_results(driver_id)
    
    reserve, driver_team = get_driver_team(driver_id)
    
    constructor_id = driver_team

    if driver_team.find('_') != -1:
        driver_team = driver_team.replace('_', ' ')
    
    driver_team = driver_team.title()
    best_race_position, total_best, total_podiums = driver_data(driver_id)
    
    img_path = f"website/static/drivers-main/{driver_id}.jpg"
    exists = False
    img_url = False
    if os.path.exists(img_path):
        exists = True
        img_url = f"/static/drivers-main/{driver_id}.jpg"
    
    team_url = f"https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/{driver_team}"
    flag_icon = f"http://purecatamphetamine.github.io/country-flag-icons/3x2/{driver_country}.svg"
    
    return render_template(
        "home-driver.html", img_src = img_url, driver_name = user.fav_driver, number = number, results = results, 
        team_url = team_url, flag_src = flag_icon, dob = dob, best_race_position = best_race_position, total_best = total_best,
        total_podiums = total_podiums, team = driver_team, champ_count = driver_champ_count, constructor_id=constructor_id,reserve=reserve, exists=exists
        )

@login_required
@views.route('/team')
def team():
    user = User.query.filter_by(id = session['user_id']).first()
    fav_team = user.fav_team
    season = datetime.datetime.now().year
    constructor = db.session.execute(
        db.select(DriverConstructor).filter_by(constructor_name = fav_team)
    ).scalar()
    
    constructor_id, year_joined, nationality, champs, wins = get_constructor(fav_team)
    
    
    fav_team_url = constructor_id
    if constructor_id.find('_') != -1:
        fav_team_url = constructor_id.replace('_', ' ')
        
    fav_team_url = fav_team_url.title()
    
    team_url = f"https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_475/content/dam/fom-website/2018-redesign-assets/team%20logos/{fav_team_url}"
    
    recent_race_id = db.session.execute(
        db.select(Result.race_id).order_by(Result.race_id.desc())
    ).scalar()
    
    races = db.session.execute(db.select(Race.race_id, Race.race_name).filter_by(season = season)).all()
    
    drivers = get_team_drivers(constructor_id)
    results = get_team_results(constructor_id, drivers)

    for driver in drivers:
        last_name = driver['name'].split()[1].lower()
        img_path = f"website/static/drivers-main/{driver['id']}.jpg"
        if os.path.exists(img_path):
            driver['img'] = f"/static/drivers-main/{driver['id']}.jpg"
        else:
            driver['img'] = False
        
    
    for race in races:
        if race.race_id not in results.keys():
            results[race.race_id] = []
        results[race.race_id].insert(0, race.race_name)    

    return render_template('team.html', team_url = team_url, team_name = fav_team, results = results, drivers = drivers, 
                           nationality=nationality, year_joined=year_joined, champs=champs, wins=wins)

@login_required
@views.route('/driver/<driver_id>')
def driver(driver_id):
    driver = db.session.execute(
        db.select(Driver).filter_by(driver_id = driver_id)
    ).scalar()
    
    first_name = driver.first_name
    last_name = driver.last_name
    number = driver.driver_num
    driver_name = ' '.join([first_name, last_name])
    dob = [driver.dob.strftime('%d'), driver.dob.strftime('%m'), driver.dob.strftime('%Y')]
    dob = ' - '.join(dob)

    for country in countries:
        if country['demonyms']['eng']['f'] == driver.nationality:
            driver_country = country['cca2'].upper()
    
    results, driver_champ_count = get_driver_results(driver_id)
    reserve, driver_team = get_driver_team(driver_id)
    
    constructor_id = driver_team
    if driver_team == 'sauber':
        driver_team = 'kick_sauber'
    
    
    
    if driver_team.find('_') != -1:
        driver_team = driver_team.replace('_', ' ')
    
    driver_team = driver_team.title()
    best_race_position, total_best, total_podiums = driver_data(driver_id)
    
    img_path = f"website/static/drivers-main/{driver_id}.jpg"
    print(img_path)
    exists = False
    img_url = False
    if os.path.exists(img_path):
        exists = True
        img_url = f"/static/drivers-main/{driver_id}.jpg"
    
    team_url = f"https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/{driver_team}"
    flag_icon = f"http://purecatamphetamine.github.io/country-flag-icons/3x2/{driver_country}.svg"
    
    return render_template(
        "home-driver.html", img_src = img_url, driver_name = driver_name, number = number, results = results, 
        team_url = team_url, flag_src = flag_icon, dob = dob, best_race_position = best_race_position, total_best = total_best,
        total_podiums = total_podiums, team = driver_team, champ_count = driver_champ_count, constructor_id=constructor_id, reserve=reserve, exists=exists
        )



@login_required
@views.route('/team/<constructor_id>')
def constructor(constructor_id):

    season = datetime.datetime.now().year
    
    team = db.session.execute(
        db.select(Constructor.constructor_name).filter_by(constructor_id = constructor_id)
    ).scalar()
    
    _, year_joined, nationality, champs, wins = get_constructor(team)
    
    
    fav_team_url = constructor_id
    
    if fav_team_url == 'sauber':
        fav_team_url = 'kick sauber'
    
    if constructor_id.find('_') != -1:
        fav_team_url = constructor_id.replace('_', ' ')
        
    fav_team_url = fav_team_url.title()
    
    team_url = f"https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_475/content/dam/fom-website/2018-redesign-assets/team%20logos/{fav_team_url}"
    
    recent_race_id = db.session.execute(
        db.select(Result.race_id).order_by(Result.race_id.desc())
    ).scalar()
    
    races = db.session.execute(db.select(Race.race_id, Race.race_name).filter_by(season = season)).all()
    
    drivers = get_team_drivers(constructor_id)
    results = get_team_results(constructor_id, drivers)
    
    for driver in drivers:
        last_name = driver['name'].split()[1].lower()
        img_path = f"website/static/drivers-main/{driver['id']}.jpg"
        
        if os.path.exists(img_path):
            driver['img'] = f"/static/drivers-main/{driver['id']}.jpg"
        else:
            driver['img'] = False
    
    for race in races:
        if race.race_id not in results.keys():
            results[race.race_id] = []
        results[race.race_id].insert(0, race.race_name)    

    return render_template('team.html', team_url = team_url, team_name = team, results = results, drivers = drivers, 
                           nationality=nationality, year_joined=year_joined, champs=champs, wins=wins)

@login_required
@views.route('/calendar')
def calendar():
    season = datetime.datetime.now().year
    current_date = datetime.datetime.now(tz=datetime.timezone.utc)
    print(current_date)
    # utc_current_date = datetime.datetime.now(datetime.timezone.utc)
    utc_current_date = current_date.timestamp()
    print(utc_current_date)
    
    schedule = db.session.execute(
        db.select(Race.round, Race.race_name, Race.date, Race.time, Circuit.circuit_name, Circuit.city, Circuit.country)
        .join(Circuit, Race.circuit_id == Circuit.circuit_id)
        .filter(Race.season == season)
    ).all()
    schedule_list = []
    for race in schedule:
        race_date = race.date.strftime("%d/%m/%y")
        race_time = race.time.strftime("%H:%M")
        
        if os.path.exists(f"website/static/track/{race.country}.png"):
            track_img = f"static/track/{race.country}.png"
        else:
            track_img = f"static/track/{race.city}.png"
        
        for country in countries:
            if race.country in country['altSpellings'] or race.country == country['name']['common'] :
                flag = country['cca2']
        
        city = race.city
        if city.find('-') != -1:
            city = city.replace('-', ' ')
            
        race_dict = {'round':race.round, 
                     'race':race.race_name, 
                     'date':race_date, 
                     'time':race_time, 
                     'city':city, 
                     'country':race.country,
                     'flag': f"http://purecatamphetamine.github.io/country-flag-icons/3x2/{flag}.svg",
                     'track_img': track_img
                     }
        
        schedule_list.append(race_dict)
    
    # Get next race
    next_race = False # season has completed

    for race in schedule:
        
        if os.path.exists(f"website/static/track/{race.country}.png"):
            track_img = f"static/track/{race.country}.png"
        else:
            track_img = f"static/track/{race.city}.png"
        
        for country in countries:
            if race.country in country['altSpellings'] or race.country == country['name']['common'] :
                flag = country['cca2']
        
        city = race.city
        if city.find('-') != -1:
            city = city.replace('-', ' ')
        
        race_date = race.date.strftime("%Y/%m/%d")    
       
        race_time = race.time.strftime("%H:%M:%S")
        
        race_date_time = f"{race_date} {race_time}"

        race_date_time = datetime.datetime.strptime(race_date_time, "%Y/%m/%d %H:%M:%S")

        race_date_time = race_date_time.replace(tzinfo=datetime.timezone.utc).timestamp()
        
        if race_date_time >= utc_current_date:
            next_race ={'round':race.round, 
                        'race':race.race_name, 
                        'date':f"{race.date}T{race_time}Z", 
                        'time':race_time, 
                        'city':city, 
                        'country':race.country,
                        'flag': f"http://purecatamphetamine.github.io/country-flag-icons/3x2/{flag}.svg",
                        'track_img': track_img
                        }
            print(next_race['date'])
            break
        
    return render_template('schedule.html', schedule = schedule_list, next_race = next_race)