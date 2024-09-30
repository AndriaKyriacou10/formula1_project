import requests
import datetime

from flask import redirect, render_template, request, session
from functools import wraps
from sqlalchemy import func, or_, and_

from . import base_url, db
from .models import *

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user_id'] is None :
            return redirect('/')
    
    return decorated_function

def get_drivers_constructors ():
    season = datetime.datetime.now().year
    round = 1 
    race_id = db.session.execute(db.Select(Race.race_id).filter_by(season = season, round = round)).scalar_one()
    
    drivers_id = db.session.execute ( 
        db.select(db.distinct(DriverConstructor.driver_id))
        .join(Race, Race.race_id == DriverConstructor.race_id)
        .filter(Race.season == season)                    
    ).scalars().all()
    
    constructors = db.session.execute (
        db.Select(db.distinct(DriverConstructor.constructor_name))
        .join(Race, Race.race_id == DriverConstructor.race_id)
        .filter(Race.season == season)    
    ).scalars().all()
    
    
    drivers = []
    for driver_id in drivers_id:
        driver = db.session.execute(
            db.select(Driver.first_name, Driver.last_name).filter_by(driver_id = driver_id)
        ).mappings().all()
        full_name = (driver[0]['first_name'], driver[0]['last_name'])
        drivers.append(' '.join(full_name))
    
    return (drivers, constructors)
                  

def get_driver_data(driver_name):
    first_name = driver_name.split()[0]
    last_name = driver_name.split()[1]
    driver = db.session.execute(
        db.select(Driver).filter_by(first_name = first_name, last_name = last_name)
    ).scalar_one()
    return driver


def get_driver_results(driver_id):
    season = datetime.datetime.now().year
    
    race_ids = db.session.execute(
        db.select(Race.race_id, Race.round).filter_by(season = season)
    ).all()
    driver_champ_count = db.session.execute(
    db.select(func.count(DriverStanding.id))
    .filter(DriverStanding.driver_id == driver_id, DriverStanding.position == 1, DriverStanding.season < season)
    ).scalar()
    
    results = []
    for race_id,round in race_ids:
        race_name = db.session.execute(
            db.select(Race.race_name).filter_by(race_id = race_id)
        ).scalar_one()
        
        result = db.session.execute(
            db.select(Result).filter_by(race_id = race_id, driver_id = driver_id)
        ).scalar_one_or_none()
        
        if result:
            result_dict = {
                'results_id': result.results_id,
                'race_id' : result.race_id,
                'race_name': race_name,
                'driver_id' : result.driver_id,
                'position' : result.position,
                'points' : result.points,
                'round' : round
            }
            results.append(result_dict) 
        
           
    return (results,driver_champ_count)
        
def get_driver_team(driver_id):
    year = datetime.datetime.now().year
    reserve = False
    recent_race_id = db.session.execute(
            db.select(Result.race_id).order_by(Result.race_id.desc())
        ).scalar()
    
    team = db.session.execute(
        db.select(DriverConstructor.constructor_id).filter_by(driver_id = driver_id, race_id = recent_race_id)
    ).scalar()
    
    if team == None:
        reserve = True
        team = db.session.execute(
            db.select(DriverConstructor.constructor_id).filter_by(driver_id = driver_id)
        ).scalar()
    
    return reserve, team

def driver_data(driver_id):
    position_all = db.session.execute(
        db.select(Result.position).filter_by(driver_id = driver_id)
    ).scalars().all()
    
    best_race_position = min(position_all)
    total_best = position_all.count(best_race_position)
    total_podiums = 0
    for position in position_all:
        if position <=3:
            total_podiums += 1
    
    return (best_race_position, total_best, total_podiums)
    


def get_constructor(fav_team):
    current_season = datetime.datetime.now().year
    constructor = db.session.execute(
        db.select(DriverConstructor).filter_by(constructor_name = fav_team)
    ).scalar()
    
    nationality = db.session.execute(
        db.select(Constructor.nationality).filter_by(constructor_id = constructor.constructor_id)
    ).scalar()
    
    champs = db.session.execute(
        db.select(func.count(ConstructorStanding.constructor_id))
        .filter(ConstructorStanding.constructor_id == constructor.constructor_id, ConstructorStanding.position == 1, ConstructorStanding.season<current_season)
    ).scalar()

    wins = db.session.execute(
        db.select(func.sum(ConstructorStanding.wins))
        .filter(ConstructorStanding.constructor_id == constructor.constructor_id)
    ).scalar()
    return (constructor.constructor_id, constructor.season, nationality, champs, wins)

def get_team_drivers(constructor_id):
    current_season = datetime.datetime.now().year
    recent_race_id = db.session.execute(
        db.select(Result.race_id).order_by(Result.race_id.desc())
    ).scalar()
    
    # drivers_id = db.session.execute(
    #     db.select(DriverConstructor.driver_id).filter_by(race_id = recent_race_id, constructor_id = constructor_id)
    # ).scalars().all()
    
    drivers_id = db.session.execute (
        db.select(db.distinct(DriverConstructor.driver_id))
        .join(Race, Race.race_id == DriverConstructor.race_id)
        .filter(Race.season == current_season)
        .filter(DriverConstructor.constructor_id == constructor_id)
    ).scalars().all()
    
    
    drivers = []
    for driver_id in drivers_id:
        driver_dict = {}
        driver = db.session.execute(
            db.select(Driver).filter_by(driver_id = driver_id)
        ).scalar()
        driver_dict['id'] = driver_id
        driver_dict['name'] = ' '.join([driver.first_name, driver.last_name])
        driver_dict['number'] = driver.driver_num
        driver_dict['nationality'] = driver.nationality
        
        drivers.append(driver_dict)
    return drivers 

def get_team_results(constructor_id, drivers):
    print(f"Drivers: {drivers} | {len(drivers)}")
    season = datetime.datetime.now().year
    
    # First race id of current season
    race_id = db.session.execute(
        db.select(Race.race_id).filter_by(season = season)
    ).scalar()
    
    result_list = []
    
    results = db.session.execute(
        db.select(Result)
        .join(DriverConstructor, DriverConstructor.id == Result.results_id)
        .filter(Result.race_id >= race_id)
        .filter(DriverConstructor.constructor_id == constructor_id)
    ).mappings().all()
    
    results_dict = {}
    for result in results:
        
        race_name = db.session.execute(db.select(Race.race_name).filter_by(race_id = result.Result.race_id)).scalar()
        race_id = result.Result.race_id
        
        if race_id not in results_dict:
            results_dict[race_id] = []
        
        driver = result.Result.driver_id
       
        if (driver).find('_') != -1:
            driver = driver.split('_')[1]
    
        for i in range(len(drivers)):
            if result.Result.driver_id == drivers[i]['id']:
                results_dict[race_id].insert(i, {'driver_id':driver, 'position':result.Result.position, 'points':result.Result.points})
    
    for key in results_dict.keys():
        if len(results_dict[key]) != 2:
            for i in range(len(drivers)):
                if drivers[i]['id'] not in results_dict[key][0]['driver_id']:
                    previous_race = db.session.execute(db.select(Result.driver_id).filter(and_(Result.race_id == key -1, Result.driver_id == drivers[i]['id']))).scalar_one_or_none()
                    if previous_race != None:
                        results_dict[key].insert(i, {'driver_id':drivers[i]['id'], 'position':'N/A', 'points':'N/A'})
    
    return results_dict