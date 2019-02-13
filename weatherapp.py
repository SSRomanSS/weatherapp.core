"""This is my first project"""


import sys
import argparse
import html
from urllib.request import urlopen, Request
from termcolor import colored
from bs4 import BeautifulSoup


ACCU_URL = 'https://www.accuweather.com/ru/ua/dnipro/322722/weather-forecast/322722'
ACCU_TAGS_TEMP = (['span', {'class': 'large-temp'}],)
ACCU_TAGS_COND = (['span', {'class': 'cond'}],)

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


def get_page_content(url):
    """

    :param url:
    :return:
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    request = Request(url, headers=headers)
    page_content = BeautifulSoup(urlopen(request), features="lxml")
    return page_content


def weather_source(input_name):
    """


    :param input_name:
    :return:
    """
    commands = {'accu': 'Accuweather',
                'rp5': 'RP5',
                'sin': 'sinoptik.ua'}
    weather_site = {'Accuweather': (ACCU_URL, ACCU_TAGS_TEMP, ACCU_TAGS_COND),
                    'RP5': (RP5_URL, RP5_TAGS_TEMP, RP5_TAGS_COND),
                    'sinoptik.ua': (SINOPTIK_URL, SINOPTIK_TAGS_TEMP, SINOPTIK_TAGS_COND)}
    if input_name == '':
        return weather_site
    if input_name in commands:
        weather_site = {commands[input_name]:
                        weather_site[commands[input_name]]}
        return weather_site
    return sys.exit('Unknown command, choice from: accu, rp5, sin')


def get_weather_info(page_content, tags):
    """

    :param page_content:
    :param tags:
    :return:
    """
    content = page_content
    if len(tags) > 1:
        for i in range(len(tags) - 1):
            content = content.find(tags[i][0], **tags[i][1])
        result = content.find(tags[-1][0], **tags[-1][1]).text

        if result == '':
            result = content.find(tags[-1][0], **tags[-1][1])['alt']
    else:
        result = content.find(tags[-1][0], **tags[-1][1]).text
    return result


def result_output(website, temperature, conditions):
    """

    :param website:
    :param temperature:
    :param conditions:
    :return:
    """
    print(colored('From {}:'.format(website), 'red'))
    print(colored('Temperature:', 'blue') + ' {}:'
          .format(html.unescape(temperature.replace(' ', ''))))
    print(colored('Weather conditions:', 'blue') +'\n{}\n'
          .format(conditions.strip()).replace(', ', '\n'))


def main(argv):
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('site', help='Website choice', nargs='?')
    if parser.parse_args(argv).site:
        input_name = parser.parse_args(argv).site
    else:
        input_name = ''

    for name in weather_source(input_name):
        url, temp_tags, cond_tags = weather_source(input_name)[name]
        page_content = get_page_content(url)
        temperature = get_weather_info(page_content, temp_tags)
        conditions = get_weather_info(page_content, cond_tags)
        result_output(name, temperature, conditions)


if __name__ == '__main__':
    main(sys.argv[1:])
