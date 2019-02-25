# -*- coding: utf-8 -*-
"""
This is weather search script
"""
import sys
import argparse
import configparser
import html
import os
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from htmldom import htmldom


ACCU_SET = 'https://www.accuweather.com/ru/browse-locations'
ACCU_LIST = (['li', {'class': 'drilldown cl'}],)
ACCU_NAME = (['em', {}],)
ACUU_LINK = (['a', {}],)
ACCU_URL = 'https://www.accuweather.com/ru/ua/dnipro/322722/weather-forecast/322722'
ACCU_TAGS_TEMP = (['span', {'class': 'large-temp'}],)
ACCU_TAGS_COND = (['span', {'class': 'cond'}],)

RP5_SET = 'http://rp5.ua'
RP5_LIST = (['div', {'class': 'country_map_links'}],
            ['h3', {}],)
RP5_NAME = (['a', {'href': True}],)
RP5_LINK = (['a', {'href': True}],)
RP5_VAR = ('div', {'class': 'city_link'})  # для додатокового пошуку на деяких кінцевих сторінквх
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
                'sin': 'sinoptik.ua'
                }
    weather_site = {'Accuweather': (ACCU_URL, ACCU_TAGS_TEMP, ACCU_TAGS_COND),
                    'RP5': (RP5_URL, RP5_TAGS_TEMP, RP5_TAGS_COND),
                    'sinoptik.ua': (SINOPTIK_URL, SINOPTIK_TAGS_TEMP, SINOPTIK_TAGS_COND)}

    if os.path.exists(get_settings_file()):
        weather_site_key = commands[get_settings()[2]]  # значення 'shortcut' із файла конфігурації
    # є ключем в словнику 'command'
        weather_site = {weather_site_key:
                        (get_settings()[1],  # URL це значення 'link' із файла конфігурації
                         *weather_site[weather_site_key][1:])}
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
            content = content.find(tags[i][0], tags[i][1])
        result = content.find(tags[-1][0], tags[-1][1]).text

        if result == '':
            result = content.find(tags[-1][0], tags[-1][1])['alt']
    else:
        result = content.find(tags[-1][0], tags[-1][1]).text
    return result


def create_parser():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('site', help='Choice website: '
                                     'accu=Accuwether, '
                                     'rp5=RP5.ua, '
                                     'sin=sinoptik.ua',
                        nargs='?', default='')
    parser.add_argument('-f', '--file', help='The name of file for output',
                        type=argparse.FileType(mode='w', encoding='utf8'))
    parser.add_argument('-s', '--settings', nargs='?')
    return parser


def create_settings(site_set):
    """

    :return:
    """
    commands = {'accu': (ACCU_SET, ACCU_LIST, ACCU_NAME, ACUU_LINK),
                'rp5': (RP5_SET, RP5_LIST, RP5_NAME, RP5_LINK),
                }
    if site_set not in commands:
        sys.exit('Unknown command, choice from: accu, rp5, reset')
    link_set, locations_list, location_name, location_link = commands[site_set]
    content = get_page_content(link_set)
    if site_set == 'rp5':  # на RP5 в структурі сторінки неповні лінки
        dom = htmldom.HtmlDom(link_set)
        dom = dom.createDom()

    while content:
        search_list = []
        if len(locations_list) == 1:
            search_content = content.find_all(locations_list[0][0], locations_list[0][1])
            if not search_content:
                search_content = content.find_all(RP5_VAR[0], RP5_VAR[1])  # для деяких кінцевих
                # сторінок з RP5, які мають іншу структуру тегів
        else:
            search_content = content.find_all(locations_list[0][0], locations_list[0][1])
            locations_list = locations_list[1:]

        ind = 0
        for i in search_content:
            print(i.find(location_name[0][0], location_name[0][1]).text, '-', ind)
            search_list.append((i.find(location_name[0][0], location_name[0][1]).text,
                                i.find(location_link[0][0], location_link[0][1])['href']))
            ind += 1
        if search_list:
            try:
                select = int(input('Make your choice, input the number:\n>'))
            except ValueError:
                sys.exit('You input not number')
            if 'http' not in search_list[select][1]:  # якщо лінк не повний
                content = get_page_content(
                    dom.baseURL + '/' +
                    quote(search_list[select][1], encoding='utf8'))  # лінк кирилицею
                link = dom.baseURL + '/' + quote(search_list[select][1])
            if 'http' in search_list[select][1]:
                content = get_page_content(search_list[select][1])
                link = search_list[select][1]
            name = search_list[select][0]
        else:
            break
    save_settings(name, link, site_set)


def get_settings_file():
    """

    :return:
    """
    return str(Path.home() / CONFIG_FILE)


def save_settings(name, link, site_set):
    """

    :param name:
    :param link:
    :param site_set:
    :return:
    """
    config = configparser.RawConfigParser()  # якшо значення конфігурації
    # зчитувати за допомогою ConfigParser,це  робить неможливим використання "%".
    # Використано RawConfigParser, щоб уникнути спеціальної обробки значень конфігурації
    config.add_section('SELECTED_LOCATION')
    config.set('SELECTED_LOCATION', 'shortcut', site_set)
    config.set('SELECTED_LOCATION', 'name', name)
    config.set('SELECTED_LOCATION', 'link', link)
    config.write(open(get_settings_file(), 'w', encoding='utf8'))


def get_settings():
    """

    :return
    """
    config = configparser.RawConfigParser()  # якшо значення конфігурації
    # зчитувати за допомогою ConfigParser,це  робить неможливим використання "%".
    # Використано RawConfigParser, щоб уникнути спеціальної обробки значень конфігурації
    config.read(get_settings_file(), encoding='utf8')
    name = config.get('SELECTED_LOCATION', 'name')
    link = config.get('SELECTED_LOCATION', 'link')
    site_set = config.get('SELECTED_LOCATION', 'shortcut')
    return name, link, site_set


def result_output(website, temperature, conditions):
    """

    :param website:
    :param temperature:
    :param conditions:
    :return:
    """
    if os.path.exists(get_settings_file()):
        print(get_settings()[0])
    else:
        print(CITY)
    print('From {}:'.format(website))
    print('Temperature: {}'
          .format(html.unescape(temperature.replace(' ', ''))))
    print('Weather conditions:' +'\n{}\n'
          .format(conditions.strip()).replace(', ', '\n'))


def file_output(result, out_file):
    """

    :param result:
    :param out_file:
    :return:
    """

    for name in result:
        if os.path.exists(get_settings_file()):
            print(get_settings()[0], file=out_file)
        else:
            print(CITY, file=out_file)
        print('From {}:\n'.format(name),
              'Temperature: {}\n'.format(html.unescape(result[name][0].replace(' ', ''))),
              'Weather conditions:\n {}\n'.format(result[name][1].strip().replace(', ', '\n')),
              file=out_file)
    out_file.close()


def main():
    """

    :return:
    """
    input_name = create_parser().parse_args(sys.argv[1:]).site
    out_file = create_parser().parse_args(sys.argv[1:]).file
    site_set = create_parser().parse_args(sys.argv[1:]).settings
    if input_name and os.path.exists(get_settings_file()):
        sys.exit('Reset the settings: [-s] reset')
    if site_set == 'reset' and os.path.exists(get_settings_file()):
        os.remove(get_settings_file())
    if site_set and site_set != 'reset':
        create_settings(site_set)
    out_dict = {}
    for name in weather_source(input_name):
        url, temp_tags, cond_tags = weather_source(input_name)[name]
        page_content = get_page_content(url)
        temperature = get_weather_info(page_content, temp_tags)
        conditions = get_weather_info(page_content, cond_tags)
        result_output(name, temperature, conditions)
        if out_file:
            out_dict[name] = (temperature, conditions)
    if out_file:
        file_output(out_dict, out_file)


if __name__ == '__main__':
    main()
