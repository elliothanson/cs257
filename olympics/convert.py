'''
convert.py
Elliot Hanson, 10/14/2021
'''

import csv

def main(): 
    with open('athlete_events.csv', mode ='r')as file:
        csv_file = csv.reader(file)
        
        athlete_information_file = open('athlete_information.csv', 'w')
        athlete_names_file = open('athlete_names.csv', 'w')
        games_file = open('games.csv', 'w')
        countries_file = open('countries.csv', 'w')
        events_file = open('events.csv', 'w')
            
        athlete_name_dictionary = {}
            
        country_dictionary = {}
            
        games_dictionary = {}
            
        events_dictionary =  {}
            
        first_line = True
            
        for lines in csv_file:
            if first_line: #since the first line of the csv only has headers, it skips the line
                 first_line = False
            else:
                athlete_information_line_to_add = []
                
                for i in range(len(lines)): #replaces all extra commas in the data with spaces
                    if ',' in lines[i]: 
                        lines[i] = lines[i].replace(',','')            

                #Breaks up the csv input into the proper fields
                athlete_id = lines[0]
                athlete_name = lines[1]
                athlete_sex = lines[2]
                athlete_age = lines[3]
                athlete_height = lines[4]
                athlete_weight = lines[5]
                athlete_country = lines[6]
                country_NOC_region = lines[7]
                games_name = lines[8]
                games_year = lines[9]
                games_season = lines[10]
                games_city = lines[11]
                sport_name = lines[12]
                event_name = lines[13]
                medal_received = lines[14]
                
                
                
                athlete_information_line_to_add.append(athlete_id)
                
                #athlete_names database
                athlete_name_id, athlete_name_dictionary = process_athlete_name(athlete_name, athlete_name_dictionary, athlete_names_file)
                
                athlete_information_line_to_add.append(athlete_name_id)
                athlete_information_line_to_add.append(athlete_sex)
                athlete_information_line_to_add.append(athlete_age)
                athlete_information_line_to_add.append(athlete_height)
                athlete_information_line_to_add.append(athlete_weight)
                
                #countries database
                country_id, country_dictionary = process_country(athlete_country, country_NOC_region, country_dictionary, countries_file)
                    
                athlete_information_line_to_add.append(country_id)
                
                #games database
                games_id, games_dictionary = process_game(games_name, games_year, games_season, games_city, games_dictionary, games_file)
      
                athlete_information_line_to_add.append(games_id)
                
                #events database
                event_id, events_dictionary = process_event(event_name, sport_name, events_dictionary, events_file)
                    
                athlete_information_line_to_add.append(event_id)
                
                athlete_information_line_to_add.append(medal_received)
                athlete_information_writer = csv.writer(athlete_information_file)
                athlete_information_writer.writerow(athlete_information_line_to_add)
                
                
        athlete_information_file.close()
        athlete_names_file.close()
        games_file.close()
        countries_file.close()
        events_file.close()

def process_athlete_name(name_to_process, current_name_dictionary, file):
    '''
    This method determines if the name it is seeing is new or has been seen before. It creates a new entry in the athlete_names table if the name is new, and then returns the proper name_id.
    '''
    
    for k in range(len(name_to_process)): #replaces all quotations in names with parentheses
        if '"' in name_to_process[k] and name_to_process.count('"') == 2:
            name_to_process = name_to_process[:k] + '(' + name_to_process[k+1:]
        elif '"' in name_to_process[k] and name_to_process.count('"') == 1:
                name_to_process = name_to_process[:k] + ')' + name_to_process[k+1:]
                                
    if name_to_process not in current_name_dictionary: #the name is new
        proper_name_id = len(current_name_dictionary) + 1 #creates a new id
        current_name_dictionary.update({name_to_process:proper_name_id}) 
        athlete_names_writer = csv.writer(file)
        athlete_names_writer.writerow([proper_name_id, name_to_process])

    else: #the name already appears in the database
        proper_name_id = current_name_dictionary.get(name_to_process)  
    
    return proper_name_id, current_name_dictionary

def process_country(country_to_process, NOC_region, current_country_dictionary, file):
    '''
    This method determines if the country it is seeing is new or has been seen before. It creates a new entry in the countries table if the name is new, and then returns the proper country_id.
    '''
    
    if country_to_process not in current_country_dictionary: #the country is new
        proper_country_id = len(current_country_dictionary) + 1 #creates a new id
        current_country_dictionary.update({country_to_process: proper_country_id}) 
        
        country_writer = csv.writer(file)
        country_writer.writerow([proper_country_id, country_to_process, NOC_region])
                        

    else: #the country already appears in the database
        proper_country_id = current_country_dictionary.get(country_to_process)

    return proper_country_id, current_country_dictionary

def process_game(name, year, season, city, current_games_dictionary, file):
    '''
    This method determines if the game it is seeing is new or has been seen before. It creates a new entry in the game table if the name is new, and then returns the proper game_id.
    '''
    
    if name not in current_games_dictionary: #the game is new
        proper_game_id = len(current_games_dictionary) + 1
        current_games_dictionary.update({name: proper_game_id}) 

        games_writer = csv.writer(file)
        games_writer.writerow([proper_game_id, name, year, season, city])
                        
                    
    else: #the game already appears in the database
        proper_game_id = current_games_dictionary.get(name)
    
    return proper_game_id, current_games_dictionary

def process_event(name, sport, current_events_dictionary, file):
    '''
    This method determines if the event it is seeing is new or has been seen before. It creates a new entry in the event table if the name is new, and then returns the proper event_id.
    '''
    
    if name not in current_events_dictionary: #the name is new
        proper_event_id = len(current_events_dictionary) + 1
        current_events_dictionary.update({name: proper_event_id}) 

        events_writer = csv.writer(file)
        events_writer.writerow([proper_event_id, name, sport])


    else: #the event already appears in the database
        proper_event_id = current_events_dictionary.get(name)

    return proper_event_id, current_events_dictionary

if __name__ == '__main__':
    main()