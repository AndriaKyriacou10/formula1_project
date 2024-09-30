# Create database modules
from . import db # from current package import db object
from sqlalchemy import Integer, String

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    fav_team = db.Column(db.String(50))
    fav_driver = db.Column(db.String(50))

class Driver(db.Model):
    def __init__(self, driver_id, first_name, last_name, driver_num, acronym, nationality, dob):
        self.driver_id = driver_id
        self.first_name = first_name
        self.last_name = last_name
        self.driver_num = driver_num
        self.acronym = acronym
        self.nationality = nationality 
        self.dob = dob
      
    driver_id = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    driver_num = db.Column(db.Integer())
    acronym = db.Column(db.String(3))
    nationality = db.Column(db.String(100))
    dob = db.Column(db.Date)

class Constructor(db.Model):
    def __init__(self, constructor_id, constructor_name, nationality):
        self.constructor_id = constructor_id
        self.constructor_name = constructor_name
        self.nationality = nationality
        
    constructor_id = db.Column(db.String(100), primary_key = True, unique = True)
    constructor_name = db.Column(db.String(100))
    nationality = db.Column(db.String(50))


class Circuit (db.Model):
    def __init__(self, circuit_id, circuit_name, city, country, season):
        self.circuit_id = circuit_id
        self.circuit_name = circuit_name
        self.city = city
        self.country = country
        self.season = season
        
    circuit_id = db.Column(db.String(100), primary_key = True, unique = True)
    circuit_name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    season = db.Column(db.Integer)


class Race(db.Model):
    def __init__(self, season, round, race_name, circuit_id, date, time):
        self.season = season
        self.round = round
        self.race_name = race_name
        self.circuit_id = circuit_id
        self.date = date
        self.time = time
        
    race_id = db.Column(db.Integer, primary_key = True)
    season = db.Column(db.Integer)
    round = db.Column(db.Integer)
    race_name = db.Column(db.String(100))
    circuit_id = db.Column(db.String(100), db.ForeignKey('circuit.circuit_id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    
    circuit = db.relationship('Circuit')

class Result(db.Model):
    def __init__(self, race_id, driver_id, position, points, grid, finishing_time, status, fastest_lap_rank, fastest_lap_time):
        self.race_id = race_id
        self.driver_id = driver_id
        self.position = position
        self.points = points
        self.grid = grid
        self.finishing_time = finishing_time
        self.status = status
        self.fastest_lap_rank = fastest_lap_rank
        self.fastest_lap_time = fastest_lap_time
        
    results_id = db.Column(db.Integer, primary_key = True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.race_id'))
    driver_id = db.Column(db.String(100), db.ForeignKey('driver.driver_id'))
    position = db.Column(db.Integer)
    points = db.Column(db.Integer)
    grid = db.Column(db.Integer)
    finishing_time = db.Column(db.String(50))
    status = db.Column(db.String(50))
    fastest_lap_rank = db.Column(db.Integer)
    fastest_lap_time = db.Column(db.String(20))
    
    race = db.Relationship('Race')
    driver = db.Relationship('Driver')
    
class DriverConstructor (db.Model):
    def __init__(self, race_id, driver_id, season, constructor_id, constructor_name):
        self.race_id = race_id
        self.driver_id = driver_id
        self.season = season
        self.constructor_id = constructor_id
        self.constructor_name = constructor_name
    
    id = db.Column(db.Integer, primary_key = True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.race_id'))
    driver_id = db.Column(db.String(100), db.ForeignKey('driver.driver_id'))
    season = db.Column(db.Integer)
    constructor_id = db.Column(db.String(100), db.ForeignKey('constructor.constructor_id'))
    constructor_name = db.Column(db.String(100))

    race = db.Relationship('Race')
    driver = db.Relationship('Driver')

class DriverStanding (db.Model):
    
    def __init__(self, season, driver_id, position, points, wins):
        self.season = season
        self.driver_id = driver_id
        self.position = position
        self.points = points
        self.wins = wins
        
    id = db.Column(db.Integer, primary_key = True)
    season = db.Column(db.Integer)
    driver_id = db.Column(db.String(100), db.ForeignKey('driver.driver_id'))
    position = db.Column(db.Integer)
    points = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    
    driver = db.Relationship('Driver')

class ConstructorStanding (db.Model):
    
    def __init__(self, season, constructor_id, position, points, wins):
        self.season = season
        self.constructor_id = constructor_id
        self.position = position
        self.points = points
        self.wins = wins
        
    id = db.Column(db.Integer, primary_key = True)
    season = db.Column(db.Integer)
    constructor_id = db.Column(db.String(100), db.ForeignKey('constructor.constructor_id'))
    position = db.Column(db.Integer)
    points = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    
    constructor = db.Relationship('Constructor')