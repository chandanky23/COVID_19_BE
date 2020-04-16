import json
import os

def todaysData(data):
  root = os.path.realpath(os.path.dirname(__name__))
  filename = os.path.join(root, 'static', 'yesterday.json')
  if os.path.exists(filename):
    os.remove(filename)
    with open(filename, 'a') as json_file:
      json.dump(data, json_file)
  else:
    with open(filename, 'a') as json_file:
      json.dump(data, json_file)