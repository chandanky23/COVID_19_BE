from flask import Flask, jsonify, request
import requests
import sys
import json

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
listOfCountriesUrl = "https://covid-19-statistics.p.rapidapi.com/regions"
reportUrl = "https://covid-19-statistics.p.rapidapi.com/reports"
total_reports_url = 'https://covid-19-statistics.p.rapidapi.com/reports/total'
country_history_url = 'https://covid-193.p.rapidapi.com/history'
country_current_stats = 'https://covid-193.p.rapidapi.com/statistics'

@app.route('/country/reports')
def index():
  requestedDate = request.args.get('date')
  response = requests.request("GET", listOfCountriesUrl, headers=headers_statistics)
  jsonData = json.loads(response.text)
  jsonData1 = json.dumps(jsonData)
  returnData=[]
  for key in jsonData:
    returnData = getReportsPerProvince(jsonData.get(key), requestedDate)
  return jsonify(jsonData)

def getReportsPerProvince(countryData, requestedDate):
  for key in countryData:
    country_iso = key.get('iso')
    country_name = key.get('name')
    dynamic_report_url = reportUrl + '&iso=' + country_iso + '&region_name=' + country_name + '&date=' + requestedDate
    province_Wise_Report = requests.request("GET", dynamic_report_url, headers=headers_statistics)
    print(province_Wise_Report)
  return ""

@app.route('/total/reports')
def total():
  requested_date = request.args.get('date')
  queryString = {"date": requested_date}
  print(queryString)
  response = requests.request("GET", total_reports_url, headers=headers_statistics, params=queryString)
  json_data = json.loads(response.text)
  return jsonify(json_data)

@app.route('/country/current')
def country_total():
  requested_country = request.args.get('country')
  requested_date = request.args.get('date')
  queryString = {"date": requested_date, "country": requested_country}

  response = requests.request("GET", country_current_stats, headers=headers_history, params=queryString)
  json_data = json.loads(response.text)
  return jsonify(json_data)

@app.route('/stats/all')
def stats_all():
  response = requests.request("GET", country_current_stats, headers=headers_history)
  json_data = json.loads(response.text)
  return jsonify(json_data)
  
if(__name__) == "__main__":
    app.run(debug=True, port=4000) #run app in debug mode on port 4000
