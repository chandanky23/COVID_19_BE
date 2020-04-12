import json
import os

def getCountryNameAndCodes():
  root = os.path.realpath(os.path.dirname(__file__))
  filename = os.path.join(root, 'static', 'countryNames.json')
  with open(filename) as country_names:
    data = json.load(country_names)
    return data

def trimName(data):
  countryNamesAndCodes = getCountryNameAndCodes()
  print(countryNamesAndCodes)
  for key in data.get('response'):
    countryName = key['country']
    textFormat = countryName.replace('-', ' ')
    key['country'] = textFormat
    for i in countryNamesAndCodes:
      if i['country_name'].lower() == textFormat.lower():
        key['flag'] = i['code']
  return data