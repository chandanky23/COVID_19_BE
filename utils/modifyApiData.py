from flask import request
import requests
import json

country_history_url = 'https://covid-193.p.rapidapi.com/history'
headers_history = {
  "x-rapidapi-host": "covid-193.p.rapidapi.com",
	"x-rapidapi-key": "wQd4zoiDbhmshWKo1W2lkTeHl1VLp1XbXr4jsn8vmhWDcfmefr"
}

def modifyApi(apiData, yesterdayDate):
  temp_obj = []
  for key in apiData.get('response'):
    queryString = {"day": yesterdayDate, "country": key['api_country_name']}
    response = requests.request("GET", country_history_url, headers=headers_history)
    json_data=json.loads(response.text)
    temp_obj.append(json_data)
      