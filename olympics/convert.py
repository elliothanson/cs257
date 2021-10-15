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
            
        athlete_name_list = []
            
        country_list = []
            
        games_list = []
            
        events_list =  []
            
        first_line = True
            
        for lines in csv_file:
            if first_line: #since the first line of the csv only has headers, it skips the line
                 first_line = False
            else:
                athlete_information_line_to_add = []
                games_line_to_add = []
                countries_line_to_add = []
                events_line_to_add = []
                
                for i in range(len(lines)):
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
                
                athlete_name_id, athlete_name_list = process_athlete_name(athlete_name, athlete_name_list, athlete_names_file)
                athlete_information_line_to_add.append(athlete_name_id)
                
                athlete_information_line_to_add.append(athlete_sex)
                athlete_information_line_to_add.append(athlete_age)
                athlete_information_line_to_add.append(athlete_height)
                athlete_information_line_to_add.append(athlete_weight)
                
                country_id, country_list = process_country(athlete_country, country_NOC_region, country_list, countries_file)
                athlete_information_line_to_add.append(country_id)
                
                games_id, games_list = process_game(games_name, games_year, games_season, games_city, games_list, games_file)
                athlete_information_line_to_add.append(games_id)
                
                event_id, events_list = process_event(event_name, sport_name, events_list, events_file)
                athlete_information_line_to_add.append(event_id)
                
                athlete_information_line_to_add.append(medal_received)
                athlete_information_writer = csv.writer(athlete_information_file)
                athlete_information_writer.writerow(athlete_information_line_to_add)
                

        athlete_information_file.close()
        athlete_names_file.close()
        games_file.close()
        countries_file.close()
        events_file.close()
                    

def process_athlete_name(name_to_process, current_name_list, file):
    '''
    This method determines if the name it is seeing is new or has been seen before. It creates a new entry in the athlete_names table if the name is new, and then returns the proper name_id.
    '''
    if name_to_process not in current_name_list: #the name is new
        current_name_list.append(name_to_process) 
        proper_id = len(current_name_list)
        athlete_names_writer = csv.writer(file)
        athlete_names_writer.writerow([proper_id, name_to_process])
                        
                    
    else: #the name already appears in the list
        proper_id = current_name_list.index(name_to_process) + 1
    
    return proper_id, current_name_list
                    
def process_country(country_to_process, NOC_region, current_country_list, file):
    '''
    This method determines if the country it is seeing is new or has been seen before. It creates a new entry in the countries table if the name is new, and then returns the proper country_id.
    '''
    if country_to_process not in current_country_list: #the country is new
        current_country_list.append(country_to_process) 
        proper_id = len(current_country_list)
        
        country_writer = csv.writer(file)
        country_writer.writerow([proper_id, country_to_process, NOC_region])
                        
                    
    else: #the country already appears in the list
        proper_id = current_country_list.index(country_to_process) + 1
    
    return proper_id, current_country_list

def process_game(game_name, year, season, city, current_game_list, file):
    '''
    This method determines if the game it is seeing is new or has been seen before. It creates a new entry in the game table if the name is new, and then returns the proper game_id.
    '''
    if game_name not in current_game_list: #the game is new
        current_game_list.append(game_name) 
        proper_id = len(current_game_list)
        
        country_writer = csv.writer(file)
        country_writer.writerow([proper_id, game_name, year, season, city])
                        
                    
    else: #the game already appears in the list
        proper_id = current_game_list.index(game_name) + 1
    
    return proper_id, current_game_list
    
                    
def process_event(event_name, sport, current_event_list, file):
    '''
    This method determines if the event it is seeing is new or has been seen before. It creates a new entry in the event table if the name is new, and then returns the proper event_id.
    '''
    if event_name not in current_event_list: #the name is new
        current_event_list.append(event_name) 
        proper_id = len(current_event_list)
        
        country_writer = csv.writer(file)
        country_writer.writerow([proper_id, event_name, sport])
                        
                    
    else: #the event already appears in the list
        proper_id = current_event_list.index(event_name) + 1
    
    return proper_id, current_event_list


            
                

if __name__ == '__main__':
    main()