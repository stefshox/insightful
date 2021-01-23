def most_common(List): 
    '''Find the most common element in a list
    
    Parameters
    ----------
    List: List

    Returns
    -------
    var: the most common element in the list
    '''
    return max(set(List), key = List.count) 

def flatten(List):
    '''Flattens list of lists (makes a uniform list)
    
    Parameters
    ----------
    List: List

    Returns
    -------
    List: the flattened list
    '''
    return [elem for subList in List for elem in subList]

def year_by_year(launches, rockets, payloads):
    '''Year by Year information about launches
    
    Parameters
    ----------
    launches: json response
        SpaceX-API GET /launches 
    rockets: json response
        SpaceX-API GET /rockets 
    payloads: json response
        SpaceX-API GET /payloads 

    Returns
    -------
    year_rocket_payload: dict
        year by year information about launches
    '''
    year = 0
    fuel = 0
    load = 0
    rocket_name = None
    load_type = []
    year_rocket_payload = []
    for launch in launches:
        # There are upcoming launches that are already scheduled with their respective rocket
        if launch["upcoming"] == False:
            year = launch["date_utc"][:4]
            # Fuel used in tons
            for rocket in rockets:
                if launch["rocket"] == rocket["id"]:
                    # Only one rocket per launch used
                    fuel = rocket["first_stage"]["fuel_amount_tons"] + rocket["second_stage"]["fuel_amount_tons"]
                    rocket_name = rocket["name"]

            # Payload weight in kg
            for payload in payloads:
                if payload["mass_kg"] != None:
                    for launch_payload in launch["payloads"]:
                        if launch_payload == payload["id"]:
                            # More than one payload per launch possible
                            load += payload["mass_kg"]
                            load_type.append(payload["type"])
                        
            year_rocket_payload.append({'year': year, 
                                        'launch_id': launch["id"], 
                                        'rocket': {'name': rocket_name, 'fuel_tons': fuel}, 
                                        'payloads': {'type': load_type, 'weight_kg': load}})

            load = 0
            load_type = []
    
    return year_rocket_payload

def general_info(year_by_year, crew_time):
    '''General information about all launches
    
    Parameters
    ----------
    year_by_year: dict
        year by year information about launches
    crew_time: str, str
        (returns 2 strings) crew member time in space, crew member eva time 

    Returns
    -------
    general_info: dict
        general information about all launches
    '''
    fuel_allTime = 0
    load_allTime = 0
    rockets = []
    payloads = []
    for instance in year_by_year:
        fuel_allTime += instance['rocket']['fuel_tons']
        load_allTime += instance['payloads']['weight_kg']
        rockets.append(instance['rocket']['name'])
        payloads.append(instance['payloads']['type'])

    full_time_space, full_eva_time = crew_time

    general_info = {'from_year': year_by_year[0]['year'], 
                    'to_year': year_by_year[-1]['year'], 
                    'fuel_used_tons': fuel_allTime, 
                    'load_transported_kg': load_allTime, 
                    'most_common_rocket': most_common(rockets), 
                    'most_common_payload': most_common(flatten(payloads)), 
                    'full_time_in_space': full_time_space, 
                    'full_eva_time': full_eva_time}

    return general_info
