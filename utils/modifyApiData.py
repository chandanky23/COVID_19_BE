import re
import locale
locale.setlocale(locale.LC_ALL, '')

def formatIntNumbers(val):
  return f'{val:n}'

def stringToInt(val):
  if(type(val) == str):
    val = re.sub('[^0-9]+', '', val)
  else:
    val
  return val
  

def stringToIntTogether(data):
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
  cases = stringToIntTogether(cases)
  deaths = stringToIntTogether(deaths)
  return apiData
