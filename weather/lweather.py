__author__ = 'Semyon'

import json

with open("new_weather.json", 'r') as myfile:
    data = myfile.read().replace('\n', '')
    dd = json.loads(data)
    print(dd)

