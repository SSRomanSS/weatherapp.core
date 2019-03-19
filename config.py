"""
Weather search script constants
"""
ACCU_SHORTCUT = 'accu'
ACCU_TITLE = 'Accuweather'
ACCU_SET = 'https://www.accuweather.com/ru/browse-locations'
ACCU_LIST = (['li', {'class': 'drilldown cl'}],)
ACCU_NAME = (['em', {}],)
ACCU_LINK = (['a', {}],)
ACCU_URL = 'https://www.accuweather.com/ru/ua/dnipro/322722/weather-forecast/322722'
ACCU_TAGS_TEMP = (['span', {'class': 'large-temp'}],)
ACCU_TAGS_COND = (['span', {'class': 'cond'}],)

RP5_SHORTCUT = 'rp5'
RP5_TITLE = 'RP5'
RP5_SET = 'http://rp5.ua'
RP5_LIST = (['div', {'class': 'country_map_links'}],
            ['h3', {}],)
RP5_NAME = (['a', {'href': True}],)
RP5_LINK = (['a', {'href': True}],)
RP5_VAR = ('div', {'class': 'city_link'})  # для додатокового пошуку на деяких кінцевих сторінках
RP5_URL = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_' \
          '%D0%94%D0%BD%D0%B5%D0%BF%D1%80%D0%B5_(%D0%94%D0%BD%D0%B5%D0%' \
          'BF%D1%80%D0%BE%D0%BF%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B5)'
RP5_TAGS_TEMP = (['div', {'class': 'ArchiveTemp'}],
                 ['span', {'class': 't_0'}])
RP5_TAGS_COND = (['div', {'id': 'archiveString'}],
                 ['div', {'class': 'ArchiveInfo'}])

SINOPTIK_URL = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0' \
               '-%D0%B4%D0%BD%D0%B5%D0%BF%D1%80-303007131'
SINOPTIK_TAGS_TEMP = (['p', {'class': 'today-temp'}],)
SINOPTIK_TAGS_COND = (['div', {'class': 'lSide'}],
                      ['div', {'class': 'img'}],
                      ['img', {'height': '150'}])

CITY = 'Dnipro'

CONFIG_FILE = 'weatherapp.ini'

CACHE_DIR = '.weather_cache'

TIME_CACHE = 300

WEATHER_SITE = {'accu': (ACCU_URL, ACCU_TAGS_TEMP, ACCU_TAGS_COND),
                'rp5': (RP5_URL, RP5_TAGS_TEMP, RP5_TAGS_COND)
                }
