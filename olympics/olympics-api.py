'''
    olympics-api.py
    Elliot Hanson, 27 October 2021
'''
import sys
import argparse
import flask
import json
import psycopg2
import config

app = flask.Flask(__name__)

@app.route('/games')
def get_games():
    ''' 
    Returns a JSON list of dictionaries, each of which represents one
    Olympic games, sorted by year. Each dictionary in this list will have
    the following fields:
        id -- (INTEGER) a unique identifier for the games in question
        year -- (INTEGER) the 4-digit year in which the games were held (e.g. 1992)
        season -- (TEXT) the season of the games (either "Summer" or "Winter")
        city -- (TEXT) the host city (e.g. "Barcelona")
    '''
    # Connect to the database and create a cursor
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
        cursor = connection.cursor()
        
    except Exception as e:
        print(e)
        exit()
    
    try:
        query = '''SELECT games.id, games.year, games.season, games.city 
                FROM games ORDER BY games.year
                '''
        cursor.execute(query)
            
    except Exception as e:
        print(e)
        exit()
    
    games_list = {}
    for row in cursor:
        games_id = row[0]
        games_year = int(row[1])
        games_season = row[2]
        games_city = row[3]
        games_list.update({games_id: {'year':games_year, 'season':games_season, 'city':games_city}})
    
    
    connection.close()

    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    ''' 
    Returns a JSON list of dictionaries, each of which represents one
    National Olympic Committee, alphabetized by NOC abbreviation. Each dictionary
    in this list will have the following fields.

        abbreviation -- (TEXT) the NOC's abbreviation (e.g. "USA", "MEX", "CAN", etc.)
        name -- (TEXT) the NOC's full name (see the noc_regions.csv file)
    '''
    # Connect to the database and create a cursor
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
        cursor = connection.cursor()
        
    except Exception as e:
        print(e)
        exit()
    
    try:
        query = '''SELECT NOC_names.abbreviation, NOC_names.country1, NOC_names.country2
                FROM NOC_names
                '''
        cursor.execute(query)
            
    except Exception as e:
        print(e)
        exit()
    
    NOC_list = {}
    for row in cursor:
        NOC_abbreviation = row[0]
        NOC_countries = row[1]
        if row[2] != '':
            NOC_countries += ' and ' + row[2]
        NOC_list.update({NOC_abbreviation: {'name':NOC_countries}})
        
    connection.close()
    
    return json.dumps(NOC_list)

@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    ''' 
    Returns a JSON list of dictionaries, each representing one athlete
    who earned a medal in the specified games. Each dictionary will have the
    following fields.

        athlete_id -- (INTEGER) a unique identifier for the athlete
        athlete_name -- (TEXT) the athlete's full name
        athlete_sex -- (TEXT) the athlete's sex as specified in the database ("F" or "M")
        sport -- (TEXT) the name of the sport in which the medal was earned
        event -- (TEXT) the name of the event in which the medal was earned
        medal -- (TEXT) the type of medal ("gold", "silver", or "bronze")

    If the GET parameter noc=noc_abbreviation is present, this endpoint will return
    only those medalists who were on the specified NOC's team during the specified
    games.

    The <games_id> is whatever string (digits or otherwise) that your database/API
    uses to uniquely identify an Olympic games.
    '''
    # Connect to the database and create a cursor
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
        cursor = connection.cursor()
        
    except Exception as e:
        print(e)
        exit()
        
    try:
        query = '''SELECT athlete_information.id, athlete_names.full_name,
                athlete_information.sex, events.sport, events.event_name, countries.NOC_region, athlete_information.medal
                FROM athlete_information, athlete_names, events, games, countries
                WHERE athlete_information.name_id = athlete_names.id AND
                athlete_information.event_id = events.id AND
                athlete_information.country_id = countries.id AND
                athlete_information.medal NOT LIKE 'NA' AND
                athlete_information.games_id = %s
                '''
        cursor.execute(query, (games_id,))

    except Exception as e:
        print(e)
        exit()
        
    NOC = flask.request.args.get('noc')
    athlete_list = {}
    for row in cursor:
        athlete_id = row[0]
        athlete_name = row[1]
        athlete_sex = row[2]
        sport = row[3]
        event = row[4]
        athlete_NOC = row[5]
        medal = row[6]
        
        if NOC is not None and NOC != athlete_NOC:
            continue
        
        athlete_list.update({athlete_id: {'athlete_name':athlete_name, 'athlete_sex':athlete_sex, 'sport':sport, 'event':event, 'medal':medal}})
        
    connection.close()
        
    return json.dumps(athlete_list)
                      
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
