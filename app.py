from flask import Flask, jsonify, request
import requests
import sys
import json
import firebaseStorage
from  utils import trimString, modifyApiData
from datetime import datetime, timedelta
import re

app = Flask(__name__)

headers_history = {
  "x-rapidapi-host": "covid-193.p.rapidapi.com",
	"x-rapidapi-key": "wQd4zoiDbhmshWKo1W2lkTeHl1VLp1XbXr4jsn8vmhWDcfmefr"
}
headers_india = {
  "x-rapidapi-host": "covid19india.p.rapidapi.com",
	"x-rapidapi-key": "wQd4zoiDbhmshWKo1W2lkTeHl1VLp1XbXr4jsn8vmhWDcfmefr"
}
headers_country = {
  "Subscription-Key": "3009d4ccc29e4808af1ccc25c69b4d5d"
}

country_history_url = 'https://covid-193.p.rapidapi.com/history'
country_current_stats = 'https://api.smartable.ai/coronavirus/stats/'
india_state_wise = 'https://covid19india.p.rapidapi.com/getIndiaStateData'

@app.route('/upload/flags/images')
def upload_flag_images():
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

@app.route('/stats/country/history')
def country_stats():
  requestedCountry = request.args.get('iso')
  url = country_current_stats + requestedCountry
  responseData = requests.request("GET", url, headers=headers_country)
  json_data = json.loads(responseData.text)
  tempObj = []
  history = json_data['stats']['history']

  for i in range(7):
    length = len(history)
    currentData = history[length - 1 - i]
    prevDayData = history[length - 1 -i - 1]
    tempObj.append(
      {
        'newCases': abs(currentData['confirmed'] - prevDayData['confirmed']),
        'newDeaths': abs(currentData['deaths'] - prevDayData['deaths']),
        'newRecoveries': abs(currentData['recovered'] - prevDayData['recovered']),
        'confirmed': currentData['confirmed'],
        'deaths': currentData['deaths'],
        'recoevered': currentData['recovered']
      }
    )

  return jsonify(tempObj)
  
if(__name__) == "__main__":
    app.run(debug=True, port=4000) #run app in debug mode on port 4000
