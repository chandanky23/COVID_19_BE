from flask import Flask, jsonify, request
import requests
import sys
import json
import firebaseStorage
from  utils import trimString, modifyApiData, saveTodaysData
from datetime import datetime, timedelta
from time import gmtime, strftime
import time
import re
import sched

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
usa_state_wise = 'https://corona.lmao.ninja/v2/states'


@app.route('/upload/flags/images')
def upload_flag_images():
  return "uploaded"

def method_todays_data_worldwide():
  response = requests.request("GET", 'https://corona.lmao.ninja/v2/countries?sort=cases')
  json_data = json.loads(response.text)
  for key in json_data:
    for i in key:
      if i != 'country' and i != 'countryInfo':
        key[i] = modifyApiData.formatIntNumbers(key[i])
  return json_data

@app.route('/stats/all')
def stats_all():
  return jsonify(method_todays_data_worldwide())

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

@app.route('/stats/country/data')
def india_stats():
  requestedCountry = request.args.get('country')
  tempData = []
  if requestedCountry.lower() == 'india':
    api_response = requests.request("GET", india_state_wise, headers=headers_india)
    json_data = json.loads(api_response.text)
    for key in json_data['response']:
      if key['active'] != None:
        key['active'] = modifyApiData.formatIntNumbers(key['active'])
        key['newDeaths'] = 'null'
        tempData.append(key)
  
  if requestedCountry.lower() == 'usa':
    api_response = requests.request("GET", usa_state_wise)
    json_data = json.loads(api_response.text)
    for key in json_data:
      tempData.append(
        {
          'active': modifyApiData.formatIntNumbers(key['active']),
          'confirmed': modifyApiData.formatIntNumbers(key['cases']),
          'deaths': modifyApiData.formatIntNumbers(key['deaths']),
          'name': key['state'],
          'newDeaths': modifyApiData.formatIntNumbers(key['todayDeaths']),
          'recovered': modifyApiData.formatIntNumbers(key['cases'] - key['deaths'] - key['active'])
        }
      )

  return jsonify(tempData)

# history data per country
@app.route('/stats/country/history')
def country_stats():
  requestedCountry = request.args.get('country')
  tempObj=[]
  for i in range(8):
    requestedDate = datetime.today() - timedelta(days=i)
    requestedDateFormatted = requestedDate.strftime('%Y-%m-%d')
    queryString={"day": requestedDateFormatted, "country": requestedCountry}
    response = requests.request("GET", country_history_url, headers=headers_history, params=queryString)
    json_data = json.loads(response.text)
    for key in json_data['response']:
      tempObj.append(key)
      break
  return jsonify(tempObj)

@app.route('/save/data')
def collect_todays_stats():
  print('called')
  dayTime = time.strftime("%p", time.gmtime())
  currentTime = time.strftime("%I", time.gmtime())
  minutes = time.strftime("%M", time.gmtime())
  if dayTime == 'pm' and int(currentTime) > 23 and int(minutes) > 45:
    todaysFinalData = stats_global()
    saveTodaysData.todaysData(todaysFinalData)
  else:
    todaysFinalData = method_todays_data_worldwide()
    saveTodaysData.todaysData(todaysFinalData)
    print('not yet more than 11:45')
  return 'saved'

# s=sched.scheduler(time.localtime, time.sleep)
# s.enterabs(time.strptime('01:15:00', '%H:%M:%S'), 1, collect_todays_stats)
# s.run()

if(__name__) == "__main__":
  app.run(debug=True, port=4000) #run app in debug mode on port 4000
