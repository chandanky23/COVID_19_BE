import re
import locale
locale.setlocale(locale.LC_ALL, '')

def formatIntNumbers(val):
  return f'{val:n}'

def stringToInt(data):
  for i in data:
    if(type(data[i]) == str):
      temp = re.sub('[^0-9]+', '', data[i])
      # data[i] = int(temp)
      data[i] = f'{int(temp):n}'
    else:
      data[i] = f'{data[i]:n}'
  return data

def modifyApi(apiData):
  temp_obj = []
  cases = apiData['cases']
  deaths = apiData['deaths']
  cases = stringToInt(cases)
  deaths = stringToInt(deaths)
  return apiData
