"""This is my first project"""


import html
from urllib.request import urlopen, Request

accu_url = 'https://www.accuweather.com/ru/ua/dnipro/322722/daily-weather-forecast/322722?day=1'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
accu_request = Request(accu_url, headers=headers)
response = urlopen(accu_request).read().decode('utf-8')
response = str(response)

tag = response.find('<span class="large-temp">')
start = tag + len('<span class="large-temp">')
temperature = ''
for chair in response[start:]:
    if chair != '<':
        temperature += chair
    else:
        break

tag = response.find('<span class="cond">')
start = tag + len('<span class="cond">')
conditions = ''
for chair in response[start:]:
    if chair != '<':
        conditions += chair
    else:
        break

print('From AccuWeather:\n')
print('Temperature: {}'.format(html.unescape(temperature)))
print('Weather conditions: {}'.format(conditions))
