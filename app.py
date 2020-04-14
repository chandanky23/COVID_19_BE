from flask import Flask, jsonify, request
import requests
import sys
import json
import firebaseStorage
from  utils import trimString, modifyApiData
from datetime import datetime, timedelta
import re

app = Flask(__name__)

headers_statistics = {
  'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
  'x-rapidapi-key': "wQd4zoiDbhmshWKo1W2lkTeHl1VLp1XbXr4jsn8vmhWDcfmefr",
  'content-type': 'application/json'
  }
headers_history = {
  "x-rapidapi-host": "covid-193.p.rapidapi.com",
	"x-rapidapi-key": "wQd4zoiDbhmshWKo1W2lkTeHl1VLp1XbXr4jsn8vmhWDcfmefr"
}
headers_india = {
  "x-rapidapi-host": "covid19india.p.rapidapi.com",
	"x-rapidapi-key": "wQd4zoiDbhmshWKo1W2lkTeHl1VLp1XbXr4jsn8vmhWDcfmefr"
}

listOfCountriesUrl = "https://covid-19-statistics.p.rapidapi.com/regions"
reportUrl = "https://covid-19-statistics.p.rapidapi.com/reports"
total_reports_url = 'https://covid-19-statistics.p.rapidapi.com/reports/total'
country_history_url = 'https://covid-193.p.rapidapi.com/history'
country_current_stats = 'https://covid-193.p.rapidapi.com/statistics'
india_state_wise = 'https://covid19india.p.rapidapi.com/getIndiaStateData'

# @app.route('/stats/all')
# def stats_all():
#   response = requests.request("GET", country_current_stats, headers=headers_history)
#   json_data = json.loads(response.text)
#   trimString.trimName(json_data)

#   # Getting todays date and yesterday to modify the api to show correct case numbers
#   currentDate = datetime.today().strftime('%Y-%m-%d')
#   yesterdayDate = datetime.today() - timedelta(days=1)
#   yesterdayDateFormat = yesterdayDate.strftime('%Y-%m-%d')
#   modifyApiData.modifyApi(json_data, yesterdayDateFormat)
#   return jsonify(json_data)

@app.route('/upload/flags/images')
def upload_flag_images():
  # firebaseStorage.upload_images();
  return "uploaded"

@app.route('/stats/all')
def stats_all():
  response = requests.request("GET", 'https://corona.lmao.ninja/countries?sort=cases')
  json_data = json.loads(response.text)
  for key in json_data:
    for i in key:
      if i != 'country' and i != 'countryInfo':
        key[i] = modifyApiData.formatIntNumbers(key[i])
  return jsonify(json_data)

@app.route('/stats/global')
def stats_global():
  tempObj=[]
  for x in range(7):
    requestedDate = datetime.today() - timedelta(days=x)
    requestedDateFormatted = requestedDate.strftime('%Y-%m-%d')
    queryString = { "day": requestedDateFormatted, "country": "all"}
    repsonse = requests.request("GET", country_history_url, headers=headers_history, params=queryString)
    json_data = json.loads(repsonse.text)
    for key in json_data['response']:
      formatedData = modifyApiData.modifyApi(key)
      tempObj.append(formatedData)
      break
  return jsonify(tempObj)

@app.route('/stats/india') 
def india_stats():
  api_response = requests.request("GET", india_state_wise, headers=headers_india)
  json_data = json.loads(api_response.text)
  return jsonify(json_data)
  
if(__name__) == "__main__":
    app.run(debug=True, port=4000) #run app in debug mode on port 4000
