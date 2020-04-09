from flask import Flask, jsonify
import requests
import sys
import json

app = Flask(__name__)

headers = {
  'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
  'x-rapidapi-key': "wQd4zoiDbhmshWKo1W2lkTeHl1VLp1XbXr4jsn8vmhWDcfmefr",
  'content-type': 'application/json'
  }


@app.route('/country/reports')
def index():
    listOfCountriesUrl = "https://covid-19-statistics.p.rapidapi.com/regions"
    response = requests.request("GET", listOfCountriesUrl, headers=headers)
    jsonData = json.loads(response.text)
    return jsonify(jsonData)

if(__name__) == "__main__":
    app.run(debug=True)