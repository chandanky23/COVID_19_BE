import json
import os

def getCountryNameAndCodes():
  root = os.path.realpath(os.path.dirname(__name__))
  filename = os.path.join(root, 'static', 'countryNames.json')
  with open(filename) as country_names:
    data = json.load(country_names)
    return data

def trimName(data):
  countryNamesAndCodes = getCountryNameAndCodes()
  for key in data.get('response'):
    countryName = key['country']
    key['api_country_name'] = countryName
    textFormat = countryName.replace('-', ' ')
    key['country'] = textFormat
    for i in countryNamesAndCodes:
      if i['country_name'].lower() == textFormat.lower():
        key['flag'] = i['code']
  return data