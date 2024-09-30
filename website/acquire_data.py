import requests
import datetime
from . import base_url, db
from .models import *

start_year = 1950
current_year = int(datetime.datetime.now().year)
json_endpoint = '.json?limit=1000'

class fetch_data_api():
    def __init__(self,app, logs):
        self.app = app
        self.logs = logs
    
    def fetch_drivers(self):
        drivers_url = (f'{base_url}/drivers{json_endpoint}')
        try:
            response = requests.get(drivers_url)
            response = response.json()
            drivers = response['MRData']['DriverTable']['Drivers']
            
            for driver in drivers:
                populate_driver_db(driver)
            
            db.session.commit() 
            self.logs.write('fetch-drivers - Completed\n')
        except requests.RequestException as e:
            print(f'Received error {e} during fetch_drivers')
            self.logs.write(f"Received error {e} during fetch_drivers\n")
            return None

    def fetch_circuits(self):
        for year in range(start_year, current_year+1):
            circuit_exists = Circuit.query.filter_by(season = year).first()
            if not circuit_exists:
                circuit_url = (f'{base_url}/{year}/circuits{json_endpoint}')
                try:
                    response = requests.get(circuit_url)
                    circuits = response.json()['MRData']['CircuitTable']['Circuits']
                    for circuit in circuits:
                        populate_circuits(circuit,year)
                    db.session.commit()
                    
                except requests.RequestException as e:
                    self.logs.write(f"Received error {e} during fetch_circuits\n")
                    print(f'Received error {e} during fetch_circuits')
                    return None
            else:
                continue
        print('Done with Circuits! ')        
        
        self.logs.write("fetch_circuits - Completed\n")
    
    def fetch_constructors(self):
        constructor_url = (f'{base_url}/constructors{json_endpoint}')
        try:
            response = requests.get(constructor_url)
            constructors = response.json()['MRData']['ConstructorTable']['Constructors']
            for constructor in constructors:
                constructor_exists = Constructor.query.filter_by(constructor_id = constructor['constructorId']).first()
                if not constructor_exists:
                    populate_constructors(constructor)
                    db.session.commit()
            
           
            self.logs.write("fetch_constructors - Completed\n")
        except requests.RequestException as e:
        
            self.logs.write(f"Received error {e} during fetch_constructors\n")
            
            print(f'Received error {e} during fetch_constructors')
            return None
    
    
    def fetch_races(self):
        for year in range(start_year, current_year+1):
            race_url = (f'{base_url}/{year}{json_endpoint}')
            try:
                response = requests.get(race_url)
                races = response.json()['MRData']['RaceTable']['Races']
                
                for race in races:
                    race_exists = Race.query.filter_by(season = year, round = race['round']).first()
                    if not race_exists:
                        populate_races(race)
                        db.session.commit()    
            except requests.RequestException as e:
            
                self.logs.write(f"Received error {e} during fetch-races\n")
                
                print(f'Received error {e} during fetch_races')
                return None
        
        self.logs.write("fetch_races - Completed\n") 
        
        
    
    
    def fetch_results_driverCon(self):
        year = datetime.datetime.now().year
        result_id = 0
        dCon_id = 0
        
        recent_url = (f'{base_url}/current/last/results{json_endpoint}')
        race_ids = db.session.execute(db.select(Result.race_id)).scalars().all()
        
        try:
            response = requests.get(recent_url)
            races = response.json()['MRData']['RaceTable']['Races']
            season = races[0]['season']
            round = races[0]['round']
            race_id = db.session.execute(db.select(Race.race_id).filter_by(season = season, round = round)).scalar()
        except requests.RequestException as e:
            self.logs.write(f"Received error {e} during fetch_races_results\n")
            return None
        
        if race_id not in race_ids:
            update_results_driver_con(race_id, races)
            self.logs.write(f"Results and Driver-Constructors - Updated\n")
            self.logs.write(f"Results and Driver-Constructors - Completed\n")
        if race_id in race_ids:
            self.logs.write(f"Results and Driver-Constructors - Completed\n")
            return
        else:
            for year in range(start_year, current_year+1):
                race_url = (f'{base_url}/{year}/results{json_endpoint}')
                try:
                    response = requests.get(race_url)
                    races = response.json()['MRData']['RaceTable']['Races']
                    for race in races:
                        race_id = db.session.execute(
                            db.select(Race.race_id).filter_by(season = race['season'], round = race['round'])
                        ).scalar_one()
                    
                        for result in race['Results']:
                            result_id +=1
                            dCon_id +=1
                            
                            result_exists = Result.query.filter_by(race_id = race_id).first()
                            result_ids = db.session.execute(db.select(Result.results_id)).scalars().all()
                            dCon_ids =  db.session.execute(db.select(DriverConstructor.id)).scalars().all()  
                            if result_id not in result_ids:
                                populate_results(result,race_id)
                                
                            
                            if dCon_id not in dCon_ids:                  
                                populate_driver_constructor(result, race_id, year)                  
                        db.session.commit()
                except requests.RequestException as e:
                    self.logs.write(f"Received error {e} during fetch_races_results\n")

        self.logs.write(f"Results and Driver-Constructors - Completed\n")
        print('Done with Results and Driver-Constructors !')
    
    def fetch_driver_standings(self):
        standings_id = 0
        
        standing_exists = db.session.execute(
            db.select(DriverStanding).filter_by(season = current_year)
        ).scalars().all()
        
        if standing_exists:
            update_driver_standings(current_year)
            self.logs.write("fetch_driver_standings - Updated\n")
        else:        
            for year in range(start_year, current_year+1):
                standings_url = (f'{base_url}/{year}/driverStandings{json_endpoint}')
                try:
                    response = requests.get(standings_url)
                    standings = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
                    
                    for standing in standings:
                        standings_id += 1
                        ids = db.session.execute(
                            db.select(DriverStanding.id)
                        ).scalars().all()
                        
                        if standings_id not in ids:
                            populate_driver_standings(standing, year)
                            
                    db.session.commit()        
                            
                except requests.RequestException as e:
                    self.logs.write(f"Received error {e} during fetch_driver_standings\n")
        
        self.logs.write("fetch_driver_standings - Completed\n")
        print('Done with driver standings !')
    
    def fetch_constructor_standings(self):
        standings_id = 0
        
        standing_exists = db.session.execute(
            db.select(ConstructorStanding).filter_by(season = current_year)
        ).scalars().all()
        
        if standing_exists:
            update_constructor_standings(current_year)
            self.logs.write("fetch_constructor_standings - Updated\n")
        else:
            for year in range(start_year, current_year+1):
                standings_url = (f'{base_url}/{year}/constructorStandings{json_endpoint}')
                try:
                    response = requests.get(standings_url)
                    standings = response.json()['MRData']['StandingsTable']['StandingsLists']
                    if len(standings) != 0:
                        standings = standings[0]['ConstructorStandings']
                        for standing in standings:
                            standings_id += 1
                            ids = db.session.execute(
                                db.select(ConstructorStanding.id)
                            ).scalars().all()
                            
                            
                            populate_constructor_standings(standing, year)
                                
                        db.session.commit()                   
                except requests.RequestException as e:
                    self.logs.write(f'Received error {e} during fetch_constructor_standings\n')
                    print(f'Received error {e} during fetch_constructor_standings')
        
        self.logs.write('fetch_constructor_standings - Completed\n')
        print('Done with constructor standings !')

def populate_driver_db(driver):
    driver_id = driver['driverId']
    first_name = driver['givenName']
    last_name = driver['familyName']
    driver_num = driver.get('permanentNumber', None)
    acronym = driver.get('code', None)
    nationality = driver['nationality']
    dob = datetime.datetime.strptime(driver['dateOfBirth'],'%Y-%m-%d').date()
    
    # ergast api added the following driver with whitespace at the end which causes errors in the program
    if driver_id == 'colapinto ':
        driver_id = 'colapinto'
    
    existing_driver = Driver.query.filter_by(driver_id=driver_id).first()
    if not existing_driver:
        driver_db = Driver(driver_id, first_name, last_name, driver_num, acronym, nationality, dob)
        db.session.add(driver_db)

def populate_constructors(constructor):
    constructor_id = constructor['constructorId']
    constructor_name = constructor['name']
    nationality = constructor['nationality']
    
    constructor_db = Constructor(constructor_id, constructor_name, nationality)
    db.session.add(constructor_db)

def populate_driver_team(team, driver_id, year):
    constuctor_id = team['constructorId']
    constuctor_name = team['name']
    
    team = DriverTeam(driver_id,year,constuctor_id,constuctor_name)
    db.session.add(team)

def populate_circuits(circuit, season):
    circuit_id = circuit['circuitId']
    circuit_name = circuit['circuitName']
    city = circuit['Location']['locality']
    country = circuit['Location']['country']

    circuit_exist = Circuit.query.filter_by(circuit_id = circuit_id).first()
    if not circuit_exist:
        circuit_db = Circuit(circuit_id, circuit_name, city, country, season)
        db.session.add(circuit_db)

def populate_races(race):
    season = race['season']
    round = race['round']
    race_name = race['raceName']
    circuit_id = race['Circuit']['circuitId']
    date = datetime.datetime.strptime(race['date'], '%Y-%m-%d').date()
    time = race.get('time', None)
    
    if time:
        time = time.rstrip('Z')
        time = datetime.datetime.strptime(time, '%H:%M:%S').time()
    
    race_exists = Race.query.filter_by(date = date).first()
    
    race_db = Race(season, round, race_name, circuit_id, date, time)
    db.session.add(race_db)
    db.session.flush()
    return race_db

def populate_results(result,race_id):
    driver_id = result['Driver']['driverId']
    position = result['position']
    points = result['points']
    grid = result['grid']
    finishing_time = result.get('Time', None)
    
    if finishing_time:
        finishing_time = finishing_time['time']
    
    status = result['status']
    
    fastest_lap_rank = result.get('FastestLap', {}).get('rank', None)
    fastest_lap_time = result.get('FastestLap', {}).get('Time', {}).get('time', None)

    if driver_id == 'colapinto ':
        driver_id = 'colapinto'
    
    result_db = Result(race_id, driver_id, position, points, grid, finishing_time, status, fastest_lap_rank, fastest_lap_time)
    db.session.add(result_db)

def populate_driver_constructor(result, race_id, season):
    driver_id = result['Driver']['driverId']
    constructor_id = result['Constructor']['constructorId']
    constructor_name = result['Constructor']['name']
    
    if driver_id == 'colapinto ':
        driver_id = 'colapinto'
    
    dCon = DriverConstructor(race_id, driver_id, season, constructor_id, constructor_name)
    
    db.session.add(dCon)

def populate_driver_standings(standing, year):
    driver_id = standing['Driver']['driverId']
    position = standing['position']
    points = standing['points']
    wins = standing['wins']
    
    if driver_id == 'colapinto ':
        driver_id = 'colapinto'
    
    standing_db = DriverStanding(year, driver_id, position, points, wins)
    db.session.add(standing_db)

def populate_constructor_standings(standing, season):
    constructor_id = standing['Constructor']['constructorId']
    position = standing['position']
    points = standing['points']
    wins = standing['wins']
    
    standing_db = ConstructorStanding(season, constructor_id, position, points, wins)
    db.session.add(standing_db)
    
def update_driver_standings(current_year):
    standings_url = (f'{base_url}/{current_year}/driverStandings{json_endpoint}')
    try:
        response = requests.get(standings_url)
        standings = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        for standing in standings:
            driver_id = standing['Driver']['driverId']
            position = standing['position']
            points = standing['points']
            wins = standing['wins'] 
            
            if driver_id == 'colapinto ':
                driver_id = 'colapinto'
            
            driver = DriverStanding.query.filter_by(season=current_year, driver_id = driver_id).first()
            
            if driver:
                driver.position = position
                driver.points = points
                driver.wins = wins 
                db.session.commit()
            else:
                populate_driver_standings(standing, current_year)
                db.session.commit()
        print('Done with updating driver standings')        
    except requests.RequestException as e:
        print(f'Received error {e} during update_driver_standings')
        return None

def update_constructor_standings(current_year):
    standings_url = (f'{base_url}/{current_year}/constructorStandings{json_endpoint}')
    try:
        response = requests.get(standings_url)
        standings = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        for standing in standings:
            constructor_id = standing['Constructor']['constructorId']
            position = standing['position']
            points = standing['points']
            wins = standing['wins']
            
            constructor = ConstructorStanding.query.filter_by(season=current_year, constructor_id = constructor_id).first()
            
            if constructor:
                constructor.position = standing['position']
                constructor.points = standing['points']
                constructor.wins = standing['wins'] 
                db.session.commit()
            else:
                populate_constructor_standings(standing, current_year)
                db.session.commit()
        print('Done with updating constructor standings')       
    except requests.RequestException as e:
        print(f'Received error {e} during update_constructor_standings')
        return None    

def update_results_driver_con(race_id, races):
    season = datetime.datetime.now().year
    results = races[0]['Results']
    for result in results:
        populate_results(result, race_id)
        populate_driver_constructor(result, race_id, season)
    
    print('Done with updating results and driver_constructor')