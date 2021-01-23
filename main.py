import markdown
import requests
from flask import Flask, request, jsonify
from general import general_info, year_by_year
from crew_time import crew_Alltime, crew_member_scrape

API = "https://api.spacexdata.com/v4"

launches_response = requests.get(API + "/launches")
launches = launches_response.json()

rockets_response = requests.get(API + "/rockets")
rockets = rockets_response.json()

payloads_response = requests.get(API + "/payloads")
payloads = payloads_response.json()

crew_resp = requests.get(API + '/crew')
crew = crew_resp.json()

# Yearly information as a dict
years = year_by_year(launches, rockets, payloads)

# full time in space, full eva time as 2 strings
crew_time = crew_Alltime(crew)

# Wikipedia information scrape as a dict
crew_mem_info = crew_member_scrape(crew)

#Flask server
app = Flask(__name__)
# Setting config tag to false, so that jsonify doesn't reorder json elements
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def index():
    with open('README.md', 'r') as markdown_file:
        content = markdown_file.read()
        #HTML
        return markdown.markdown(content)

# General Information
@app.route('/general', methods=['GET'])
def generaly():
    return jsonify(general_info(years, crew_time))

# Yearly Information
@app.route('/year/all', methods=['GET'])
def yearly():
    return jsonify(years)

@app.route('/year', methods=['GET'])
def per_year():
    if 'year' in request.args:
        year = request.args['year']
    else:
        return "Error: No year provided. Please specify year."

    results = []
    for elem in years:
        if elem['year'] == year:
            results.append(elem)

    return jsonify(results)

# Crew member information
@app.route('/crew-member/all', methods=['GET'])
def crew_mems():
    return jsonify(crew_mem_info)

@app.route('/crew-member', methods=['GET'])
def crew_mem():
    if 'name' in request.args:
        name = request.args['name']
    else:
        return "Error: No name provided. Please specify a name."

    results = []
    for elem in crew_mem_info:
        if elem['name'] == name:
            results.append(elem)

    return jsonify(results)

if __name__ == "__main__":
    app.run()
