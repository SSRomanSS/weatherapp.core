"""This is my first project"""


import html
from urllib.request import urlopen, Request

ACCU_URL = 'https://www.accuweather.com/ru/ua/dnipro/322722/weather-forecast/322722'
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')
RP5_URL = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0' \
          '_%D0%B2_%D0%94%D0%BD%D0%B5%D0%BF%D1%80%D0%B5' \
          '_(%D0%94%D0%BD%D0%B5%D0%BF%D1%80%D0%BE%D0%BF%D0' \
          '%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B5)'
RP5_TAGS = ('style="display: block;">', '<div id="ftab_1_content"',
            '<div class="underTitle">', """onmouseover="tooltip(this, '<b>""")
SINOPTIK_URL = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0' \
               '-%D0%B4%D0%BD%D0%B5%D0%BF%D1%80-303007131'
SINOPTIK_TAGS = ('<p class="today-temp">', 'jpg" alt="')


def get_page_content(url):
    """

    :param url:
    :return:
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    request = Request(url, headers=headers)
    page_content = str(urlopen(request).read().decode('utf-8'))
    return page_content


def get_temperature_info(page_content, temperature_tag):
    """

    :param page_content:
    :param temperature_tag:
    :return:
    """
    ind = page_content.find(temperature_tag)
    start = ind + len(temperature_tag)
    temperature_value = ''
    for chair in page_content[start:]:
        if chair != '<':
            temperature_value += chair
        else:
            temperature_value = temperature_value.replace(' ', '').replace('C', '')
            break
    return temperature_value


def get_conditions_info(page_content, conditions_tags):
    """

    :param page_content:
    :param conditions_tags:
    :return:
    """
    content = page_content
    for i in range(len(conditions_tags)):
        ind = content.find(conditions_tags[i])
        start = ind + len(conditions_tags[i])
        content = content[start:]
    conditions_value = ''
    for chair in content:
        if chair not in '"<':
            conditions_value += chair
        else:
            break
    return conditions_value


def result_output(website, temperature, conditions):
    """

    :param website:
    :param temperature:
    :param conditions:
    :return:
    """
    print('From {}:'.format(website))
    print('Temperature: {}'.format(html.unescape(temperature)))
    print('Weather conditions: {}\n'.format(conditions))


def main():
    """

    :return:
    """
    weather_sites = {'Accuweather': (ACCU_URL, ACCU_TAGS),
                     'rp5.ua': (RP5_URL, RP5_TAGS),
                     'sinoptik.ua': (SINOPTIK_URL, SINOPTIK_TAGS)}
    for name in weather_sites:
        url, tags = weather_sites[name]
        temperature_tag = tags[0]
        conditions_tags = tags[1:]
        page_content = get_page_content(url)
        temperature = get_temperature_info(page_content, temperature_tag)
        conditions = get_conditions_info(page_content, conditions_tags)
        result_output(name, temperature, conditions)


if __name__ == '__main__':
    main()
