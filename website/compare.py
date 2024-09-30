from flask import Blueprint, request, render_template, redirect, flash, url_for, jsonify, current_app
import re
import datetime
import os
from .helpers import *
from .models import *
from . import db
from . import countries
from sqlalchemy import or_, and_
compare = Blueprint('compare', __name__)

current_season = datetime.datetime.now().year

@login_required
@compare.route('/compare')
def compare_drivers():
    return render_template("compare.html")

@compare.route('/compare/search')
def search_compare():
    driver=request.args.get('q')
    search = f"%{driver}%"
    
    drivers= []
    if len(driver) >= 2 :
        if driver.find(' ') != -1:
            first_name = f"{driver.split()[0]}"
            last_name = f"{driver.split()[1]}%"
            result = db.session.execute(
                db.select(Driver.first_name, Driver.last_name)
                .filter( and_(Driver.first_name.like(first_name), Driver.last_name.like(last_name))).limit(5)
                ).all()
        else:
            result = db.session.execute(
                db.select(Driver.first_name, Driver.last_name)
                .filter( or_(Driver.first_name.like(search), Driver.last_name.like(search))).limit(5)
                ).all()
        
        for d in result:
            driver_dict = {'name': f"{d[0]} {d[1]}"}
            drivers.append(driver_dict)
        
    return jsonify(drivers)

@compare.route('/compare/results', methods = ['POST'])
def result_compare():
    if request.method == 'POST':
        driver1 = request.form.get('driver1')
        driver2 = request.form.get('driver2')

        if (not driver1) or (not driver2):
            flash('Both inputs are required', category='error')
            return redirect(url_for('compare.compare_drivers'))
        elif (driver1 == driver2):
            flash('Drivers must be different', category='error')
            return redirect(url_for('compare.compare_drivers'))
        elif (len(driver1.split()) <= 1) or (len(driver2.split()) <= 1):
            flash('Please enter a valid driver name', category='error')
            return redirect(url_for('compare.compare_drivers'))
        else:
            d1_exists = db.session.execute(
                db.select(Driver)
                .filter(and_(Driver.first_name == driver1.split()[0], Driver.last_name == driver1.split()[1]))
            ).scalar_one_or_none()
            
            d2_exists = db.session.execute(
                db.select(Driver)
                .filter(and_(Driver.first_name == driver2.split()[0], Driver.last_name == driver2.split()[1]))
            ).scalar_one_or_none()
            
            if (d1_exists == None or d2_exists == None):
                flash('Please enter a valid driver name', category='error')
                return redirect(url_for('compare.compare_drivers'))
            
            driver1_data = get_driver_data(driver1)
            driver2_data = get_driver_data(driver2)

            dob1 = '-'.join([driver1_data.dob.strftime('%d'), driver1_data.dob.strftime('%m'), driver1_data.dob.strftime('%Y')])
            dob2 = '-'.join([driver2_data.dob.strftime('%d'), driver2_data.dob.strftime('%m'), driver2_data.dob.strftime('%Y')])

            driver1_dict = {'id':driver1_data.driver_id, 'name':driver1, 'number':driver1_data.driver_num, 'nationality':driver1_data.nationality, 'dob':dob1}
            driver2_dict = {'id':driver2_data.driver_id, 'name':driver2, 'number':driver2_data.driver_num, 'nationality':driver2_data.nationality, 'dob':dob2}

            drivers = [driver1_dict, driver2_dict]
            for driver in drivers:
                # Number of wins
                driver['wins'] = db.session.execute(
                    db.select(func.sum(DriverStanding.wins))
                    .filter(DriverStanding.driver_id == driver['id'])    
                ).scalar()
                
                # Number of podiums
                driver['podiums'] = db.session.execute(
                    db.select(func.count(Result.race_id))
                    .filter(Result.driver_id == driver['id'])
                    .filter(Result.position <= 3)
                ).scalar()
                
                # Number of pole positions
                driver['pole_pos'] = db.session.execute(
                    db.select(func.count(Result.race_id))
                    .filter(Result.driver_id == driver['id'])
                    .filter(Result.grid == 1)
                ).scalar()
                
                # Number of gp enrties
                driver['gp_num'] = db.session.execute(
                    db.select(func.count(db.distinct(Result.race_id)))
                    .filter(Result.driver_id == driver['id'])
                    .filter(Result.status != 'Disqualified')
                    .filter(Result.status != 'Not classified')
                ).scalar()

                # First Race
                race = db.session.execute(
                    db.select(Race)
                    .join(Result, Result.race_id == Race.race_id)
                    .filter(Result.driver_id == driver['id'])
                    .limit(1)
                ).scalar()
                
                driver['first_race'] = f"{race.date.strftime("%d")}/{race.date.strftime("%m")}/{race.date.strftime("%Y")}"
                
                # Driver Image
                img_path = os.path.join(current_app.root_path,'static', 'drivers', f"{driver['id']}.jpg")
                if os.path.exists(img_path):
                   driver['img_url'] = f"/static/drivers/{driver['id']}.jpg"
                else:
                    driver['img_url'] = f"/static/drivers/generic-f1-driver-2.png"
                
                # Country Image
                for country in countries:
                    if country['demonyms']['eng']['f'] == driver['nationality']:
                        driver_country = country['cca2'].upper()
                        
                
                driver['flag'] = f"http://purecatamphetamine.github.io/country-flag-icons/3x2/{driver_country}.svg"
                
                # Teams
                driver['teams'] = []
                teams = db.session.execute(
                    db.select(db.distinct(DriverConstructor.constructor_id ).label('constructor_id'), DriverConstructor.constructor_name)
                    .filter(DriverConstructor.driver_id == driver['id'])
                ).mappings().all()
                
                for team in teams:
                   years = db.session.execute(
                       db.select(DriverConstructor.season)
                       .filter(DriverConstructor.constructor_id == team.constructor_id)
                       .filter(DriverConstructor.driver_id == driver['id'])
                   ).scalars().all()
                   start = f"{years[0]}"
                   end = (f"{years[-1]}" if years[-1] != current_season else 'Now')
                   
                   years = (f"{start} - {end}" if start != end else f"{start}")
                   driver['teams'].append({'team': team.constructor_name, 'years': years}) 
                
                # Championships
                champs = db.session.execute(
                    db.select(func.count(DriverStanding.id))
                    .filter(DriverStanding.driver_id == driver['id'])
                    .filter(DriverStanding.position == 1)
                    .filter(DriverStanding.season < current_season)
                ).scalar()
                
                if champs :
                    champ_years = db.session.execute(
                        db.select(DriverStanding.season)
                        .filter(DriverStanding.driver_id == driver['id'])
                        .filter(DriverStanding.position == 1)
                        .filter(DriverStanding.season < current_season)
                    ).scalars().all()
                    driver['champs'] = {'best':1, 'years':champ_years, 'count':champs}
                   
                else:
                    best_position = db.session.execute(
                        db.select(DriverStanding.position)
                        .filter(DriverStanding.driver_id == driver['id'])
                        .filter(DriverStanding.season <= current_season)
                        .order_by(DriverStanding.position.asc())
                        .limit(1)
                    ).scalar()
                    
                    best_years = db.session.execute(
                        db.select(DriverStanding.season)
                        .filter(DriverStanding.driver_id == driver['id'])
                        .filter(DriverStanding.position == best_position)
                        .filter(DriverStanding.season <= current_season)
                    ).scalars().all()
                    driver['champs'] = {'best':best_position, 'years':best_years, 'count':len(best_years)}  
                
                years = [str(year) for year in driver['champs']['years']]      
                driver['champs']['years'] = ' '.join(years)
                
                # Points
                driver['points'] = db.session.execute(
                    db.select(func.sum(DriverStanding.points))
                    .filter(DriverStanding.driver_id == driver['id'])     
                ).scalar()
                
                # Fastest Laps
                driver['fastest_laps'] = db.session.execute(
                    db.select(func.count(Result.race_id))
                    .filter(Result.driver_id == driver['id'])
                    .filter(Result.fastest_lap_rank == 1)
                ).scalar()
                
                race_id_fastest = db.session.execute(
                    db.select(Result.race_id)
                    .filter(Result.fastest_lap_rank != 0)
                    .limit(1)
                ).scalar()
                
                all_race_ids = db.session.execute(
                    db.select(Result.race_id)
                    .filter(Result.driver_id == driver['id'])
                ).scalars().all()
                
                fastest_lap_available = False
                for race_id in all_race_ids:
                    if (race_id >= race_id_fastest):
                        fastest_lap_available = True
                        break
                if not fastest_lap_available:
                    driver['fastest_laps'] = 'N/A'
                
                driver['win_ratio'] = "%.2f" % ((driver['wins']/driver['gp_num'])*100)
                driver['podium_ratio'] = "%.2f" % ((driver['podiums']/driver['gp_num'])*100)
            
            driver_data_keys = [{'key':'first_race','title':'debut race'},
                                {'key':'gp_num','title':'grand prix entries'},
                                {'key':'points','title':'points'},
                                {'key':'wins','title':'wins'},
                                {'key':'podiums','title':'podiums'},
                                {'key':'pole_pos','title':'pole positions'},
                                {'key':'fastest_laps','title':'fastest laps'}
                                ]
            return render_template('compare-result.html', drivers = drivers, driver_data_keys = driver_data_keys)

@compare.route('/compare/plots')
def compare_plots():
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    driver_ids = [id1, id2]
    
    seasons = []
    points = []
    for driver_id in driver_ids:
        season_points = db.session.execute(
            db.select(DriverStanding.season, DriverStanding.points)
            .filter(DriverStanding.driver_id == driver_id)
        ).all()

        seasons_temp = []
        points_temp = []
        for season_p in season_points:
           season, p = season_p
           seasons_temp.append(season)
           points_temp.append(p)
        

        seasons.append(seasons_temp)
        points.append(points_temp)
        

    return jsonify({'seasons':seasons, 'points':points})