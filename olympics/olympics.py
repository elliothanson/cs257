'''
   olympics.py
   Elliot Hanson, 10/20/2021
'''

import argparse
import psycopg2
import config

def display_usage():
    '''Prints out the usage statement for books.py'''
    f = open('usage.txt', 'r')
    usage_statement = f.read()
    print(usage_statement)
    f.close()

def display_NOC_athletes(cursor):
    '''
    Prints out the names of athletes who competed for a particular NOC.
    For example:
    |              Full Name              |
      Aarno Aksel (Arno) Almqvist
      Abdul-Rashid Bulayevich Sadulayev
      ...
    '''
    print('|              Full Name              |')
    no_games = True
    for row in cursor:
        no_games = False
        print('  ' + row[0])
        
    if no_games:
        print('No athletes were recorded as competing for this particular NOC.')
    print()

def display_NOC_gold_medals(cursor):
    '''
    Prints out the amount of gold medals awarded to each NOC region.
    For example:
    | NOC |  Gold Medals  |
      USA    2636
      URS    1080
      ...
    '''
    
    print('| NOC |  Gold Medals  |')
    for row in cursor:
        print('  ' + row[0] + '    ' + str(row[1]))

    print()
    

def display_games_information(cursor):
    '''
    Prints out information on certain olympic games.
    For example:
    | Year |  Season  |           City           |
      2000    Summer     Sydney
    '''
    print('| Year |  Season  |           City           |')
    no_games = True
    for row in cursor:
        no_games = False
        print('  ' + row[0] + '    ' + row[1] + '     ' + row[2])
        
    if no_games:
        print('No Olympic Games were recorded as taking place this year')
    print()

def main():
    # Connect to the database and create a cursor
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
        cursor = connection.cursor()
        
    except Exception as e:
        print(e)
        exit()
    
    parser = argparse.ArgumentParser(add_help = False)
    
    parser.add_argument('-h', '-?', '--help', action = 'store_true', dest = 'request_help')
    parser.add_argument('--NOC_athletes', type = str, dest = 'search_NOC_athletes', nargs = '?')
    parser.add_argument('--NOC_gold_medals', action = 'store_true', dest = 'search_NOC_medals')
    parser.add_argument('--games_information', type = str, dest = 'search_game', nargs = '?')
    
    args = parser.parse_args()
    
    if args.request_help: 
        display_usage()
        
    elif args.search_NOC_athletes is not None:
        try:
            query = '''SELECT DISTINCT athlete_names.full_name
                FROM athlete_names, athlete_information, countries
                WHERE athlete_information.name_id = athlete_names.id AND
                athlete_information.country_id = countries.id AND
                countries.NOC_region = %s
                '''
            cursor.execute(query, (args.search_NOC_athletes,))
            
        except Exception as e:
            print(e)
            exit()
        
        display_NOC_athletes(cursor)

    elif args.search_NOC_medals:
        try:
            query = '''SELECT countries.NOC_region, COUNT(athlete_information.id)
                    FROM countries, athlete_information
                    WHERE athlete_information.medal LIKE 'Gold' AND
                    athlete_information.country_id = countries.id
                    GROUP BY countries.NOC_region
                    ORDER BY COUNT(athlete_information.id) DESC;
                    '''
            cursor.execute(query)
        
        except Exception as e:
            print(e)
            exit()
        
        display_NOC_gold_medals(cursor)

    elif args.search_game is not None:
        try:
            query = '''SELECT games.year, games.season, games.city 
                FROM games
                WHERE games.year = %s
                '''
            cursor.execute(query, (args.search_game,))
        
        except Exception as e:
            print(e)
            exit()
        
        display_games_information(cursor)
    
    else:
        display_usage()
    
    connection.close()
    
if __name__ == '__main__':
    main()