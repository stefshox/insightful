import requests
from bs4 import BeautifulSoup
import re

def crew_member_scrape(crew):
    '''Scrape wikipedia pages of all crew members
    
    Parameters
    ----------
    crew: json response
        SpaceX-API GET /crew 

    Returns
    -------
    crew_member: dict
        crew member information
    '''
    crew_member = []
    for astronaut in crew:
        wiki = astronaut['wikipedia']
        wiki_response = requests.get(wiki)
        soup = BeautifulSoup(wiki_response.content, 'html.parser')
        table_div = soup.find(class_="infobox biography vcard")
        age_div = table_div.find(class_="noprint ForceAgeToShow")
        # Using regex to find the digits in the string
        age = int(re.findall(r'\d+', age_div.string)[0])
        time_div = table_div.find("div", text="Time in space")
        time_in_space = None
        if time_div != None:
            tr_tag = time_div.parent
            td = tr_tag.findNext('td')
            time_in_space = td.string
        else:
            time_in_space = 'No Information'

        time_div = table_div.find("div", text="Total EVA time")
        total_eva_time = None
        if time_div != None:
            tr_tag = time_div.parent
            td = tr_tag.findNext('td')
            total_eva_time = td.string
        else:
            total_eva_time = 'No Information'
        
        crew_member.append({'name': astronaut['name'], 
                            'age': age, 
                            'time_in_space': time_in_space, 
                            'total_eva_time': total_eva_time})

    return crew_member

def full_space_time(crew_members):
    '''Calculate full time in space for the entire crew
    
    Parameters
    ----------
    crew_members: dict
        crew_member_scrape() method return 

    Returns
    -------
    str: str
        full time in space for the entire crew as a string: years days hours minutes,
        additionally adds how many are currently in space in brackets
    '''
    days = []
    hours = []
    minutes = []
    currently_in_space = 0
    for member in crew_members:
        if member['time_in_space'] != None and member['time_in_space'] != 'No Information':
            # Using regex to find the digits in the string
            digits = re.findall(r'\d+', member['time_in_space'])

            if digits:
                if len(digits) == 3:
                    days.append(int(digits[0]))
                    hours.append(int(digits[1]))
                    minutes.append(int(digits[2]))
                elif len(digits) == 2:
                    hours.append(int(digits[0]))
                    minutes.append(int(digits[1]))
                elif len(digits) == 1:
                    minutes.append(int(digits[0]))
            if member['time_in_space'] == 'Currently in space':
                currently_in_space += 1
    daysNum, hoursNum, minutesNum = sum(days), sum(hours), sum(minutes)
    
    hoursNum = hoursNum + (minutesNum // 60)
    minutesNum = minutesNum % 60
    daysNum = daysNum + (hoursNum // 24)
    hoursNum = hoursNum % 24
    yearNum = daysNum // 365
    daysNum = daysNum % 365

    return str(yearNum) + 'y ' + str(daysNum) + 'd ' + str(hoursNum) + 'h ' + str(minutesNum) + 'm ' + f'({currently_in_space} Currently in space)'

def full_eva_time(crew_members):
    '''Calculate full time in space for the entire crew
    
    Parameters
    ----------
    crew_members: dict
        crew_member_scrape() method return

    Returns
    -------
    str: str
        full eva time for the entire crew as a string: days hours minutes
    '''
    days = []
    hours = []
    minutes = []
    for member in crew_members:
        if member['total_eva_time'] != None and member['total_eva_time'] != 'No Information':
            # Using regex to find the digits in the string
            digits = re.findall(r'\d+', member['total_eva_time'])

            if digits:
                if len(digits) == 3:
                    days.append(int(digits[0]))
                    hours.append(int(digits[1]))
                    minutes.append(int(digits[2]))
                elif len(digits) == 2:
                    hours.append(int(digits[0]))
                    minutes.append(int(digits[1]))
                elif len(digits) == 1:
                    minutes.append(int(digits[0]))

    daysNum, hoursNum, minutesNum = sum(days), sum(hours), sum(minutes)
    
    hoursNum = hoursNum + (minutesNum // 60)
    minutesNum = minutesNum % 60
    daysNum = daysNum + (hoursNum // 24)
    hoursNum = hoursNum % 24

    return str(daysNum) + 'd ' + str(hoursNum) + 'h ' + str(minutesNum) + 'm'

def crew_Alltime(crew):
    '''Calculate full time in space and full eva time
    
    Parameters
    ----------
    crew: json response
        SpaceX-API GET /crew  

    Returns
    -------
    str, str: str, str
        full time in space, full eva time
    '''
    crew_members = crew_member_scrape(crew)
    return full_space_time(crew_members), full_eva_time(crew_members)
