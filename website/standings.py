from flask import Blueprint, request, render_template, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import re
import datetime
from sqlalchemy.exc import IntegrityError

from .helpers import *
from .models import *
from . import db

from . import countries

standings = Blueprint('standings', __name__)

@login_required
@standings.route('/standings/driver')
def driver_standings():
    season = datetime.datetime.now().year
    
    standings = db.session.execute(
        db.select(DriverStanding).filter_by(season = season).order_by(DriverStanding.points.desc())
    ).scalars().all()
    
    # Get reasent round
    race_id = db.session.execute(
        db.select(Result.race_id).order_by(Result.race_id.desc())
    ).scalar()
    
    round = db.session.execute(
        db.select(Race.round).filter_by(race_id = race_id)
    ).scalar()
    
    standing_list = []
    for standing in standings:
        driver_name = db.session.execute(db.select(Driver.first_name, Driver.last_name).filter_by(driver_id = standing.driver_id)).first()
        driver_name = ' '.join(driver_name)
        
        standing_dict = {
                            'name': driver_name, 
                            'position': standing.position, 
                            'points': standing.points,
                            'id': standing.driver_id
                        }
        standing_list.append(standing_dict)
    
    return render_template('driver_standings.html', standings = standing_list, round = round)

@login_required
@standings.route('/standings/constructor')
def constructor_standings():
    season = datetime.datetime.now().year
    
    standings = db.session.execute(
        db.select(ConstructorStanding).filter_by(season = season).order_by(ConstructorStanding.points.desc())
    ).scalars().all()
    
    # Get recent round
    race_id = db.session.execute(
        db.select(Result.race_id).order_by(Result.race_id.desc())
    ).scalar()
    
    round = db.session.execute(
        db.select(Race.round).filter_by(race_id = race_id)
    ).scalar()
    
    standing_list = []
    for standing in standings:
        con_name = db.session.execute(db.select(Constructor.constructor_name).filter_by(constructor_id = standing.constructor_id)).scalar()

        standing_dict = {
                            'name': con_name, 
                            'position': standing.position, 
                            'points': standing.points,
                            'id': standing.constructor_id
                        }
        
        standing_list.append(standing_dict)
        
    return render_template('constructor_standings.html', standings = standing_list, round = round)