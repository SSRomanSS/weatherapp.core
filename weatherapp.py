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
temperature_accu = ''
for chair in response[start:]:
    if chair != '<':
        temperature_accu += chair
    else:
        break

tag = response.find('<span class="cond">')
start = tag + len('<span class="cond">')
conditions_accu = ''
for chair in response[start:]:
    if chair != '<':
        conditions_accu += chair
    else:
        break

rp5_url = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0' \
          '_%D0%B2_%D0%94%D0%BD%D0%B5%D0%BF%D1%80%D0%B5' \
          '_(%D0%94%D0%BD%D0%B5%D0%BF%D1%80%D0%BE%D0%BF%D0' \
          '%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B5)'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
rp5_request = Request(rp5_url, headers=headers)
response = urlopen(rp5_request).read().decode('utf-8')
response = str(response)

tag = response.find('style="display: block;">')
start = tag + len('style="display: block;">')
temperature_rp5 = ''
for chair in response[start:]:
    if chair != '<':
        temperature_rp5 += chair
    else:
        break

today = response.rfind('<b class="noprint">Сегодня</b>')
response = response[today:]
weather_cond = response.find('<a id="t_cloud_cover" href=')
response = response[weather_cond:]
start = response.find("""onmouseover="tooltip(this, '<b>""")\
        + len("""onmouseover="tooltip(this, '<b>""")
conditions_rp5 = ''
for chair in response[start:]:
    if chair != '<':
        conditions_rp5 += chair
    else:
        break

print('From AccuWeather:')
print('Temperature: {}'.format(html.unescape(temperature_accu)))
print('Weather conditions: {}\n'.format(conditions_accu))
print('From rp5.ua:')
print('Temperature: {}'.format(html.unescape(temperature_rp5)))
print('Weather conditions: {}'.format(conditions_rp5.capitalize()))
