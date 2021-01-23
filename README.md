# INSIGHTful - a RESTful API based on the SpaceX-API

_Tested on MacOS Big Sur, Ubuntu 18.04 (LTS) and Windows 10 Education Edition_

A RESTful API that gives more insight on the information given from the SpaceX-API

## Usage  

Start docker container with a python image and flask development server ("sudo" before command for Linux users if needed)

```  
docker-compose up
```  

Accessible at (also shows README):

_On MacOS and Linux:_

```
http://0.0.0.0:5000/
```  

_On Windows:_

```  
http://localhost:5000/
```

## Requirements

1. Docker Engine for Linux / Docker desktop for MacOS and Windows
2. docker-compose (for Linux) (version > 1.27.0)

### General information

```
GET /general
```

#### Form

- Start year
- Last year
- Fuel used in total in tons
- Load transported in total in kg
- Most used rocket
- Most common payload
- Total space in time of crew members
- Total EVA time of crew members

#### __Example__  

```json
{"from_year":"2006",
 "to_year":"2021",
 "fuel_used_tons":54323.4,
 "load_transported_kg":612211.55,
 "most_common_rocket":"Falcon 9",
 "most_common_payload":"Satellite",
 "full_time_in_space":"2y 64d 2h 54m (4 Currently in space)",
 "full_eva_time":"5d 13h 11m"}
```

### Yearly information

Details about all years  

```
GET /year/all
```  

Single year details (multiple launches per year = multiple responses) 

```
GET /year?year=
```  


#### __Form__

- Year
- Launch id
- Rocket
    - Rocket name
    - Fuel used in tons
- Payload
    - Payload types (can be multiple)
    - Payload weight (sum of the weight of all of the payload types during this launch)

#### __Example__  

```json  
[{"year":"2006",
  "launch_id":"5eb87cd9ffd86e000604b32a",
  "rocket":{"name":"Falcon 1",
           "fuel_tons":47.68},
  "payloads":{"type":["Satellite"],
              "weight_kg":20}}]
```

### Crew Members

Details about all crew members  

```
GET /crew-member/all
```  

Single crew member details  

```
GET /crew-member?name=
```  

#### __Form__

- Name
- Age
- Time in space (if available)
- Total EVA time (if available)

#### __Example__  

```json
[{"name":"Robert Behnken",
  "age":50,
  "time_in_space":"93d 11h 42min",
  "total_eva_time":"61 hours, 10 minutes"}]
```
