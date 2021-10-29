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
    ''' Returns a JSON list of dictionaries, each of which represents one
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
        print(row)
        games_id = row[0]
        games_year = int(row[1])
        games_season = row[2]
        games_city = row[3]
        games_list.update({games_id: {"year":games_year, "season":games_season, "city":games_city}})
    
    
    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    ''' Returns a JSON list of dictionaries, each of which represents one
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
        query = '''SELECT games.id, games.year, games.season, games.city 
                FROM games ORDER BY games.year
                '''
        cursor.execute(query)
            
    except Exception as e:
        print(e)
        exit()
    
    games_list = {}
    for row in cursor:
        print(row)
        games_id = row[0]
        games_year = int(row[1])
        games_season = row[2]
        games_city = row[3]
        games_list.update({games_id: {"year":games_year, "season":games_season, "city":games_city}})
    
    
    return json.dumps(games_list)
                      
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
