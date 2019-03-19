# -*- coding: utf-8 -*-
"""
Weather providers
"""
import configparser
import hashlib
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
from htmldom import htmldom

import config


class WeatherProvider:
    """
    Common WeatherProvider
    """

    def __init__(self, app):
        """

        :param app
        """
        self.app = app

    def get_page_content(self, url, refresh):
        """

        :param url:
        :param refresh:
        :return:
        """
        if self.get_cache(url) and self.cache_lifetime(url) and refresh is False:
            content = self.get_cache(url)
        else:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            request = Request(url, headers=headers)
            content = urlopen(request).read()
            self.save_cache(url, content)
        page_content = BeautifulSoup(content, features="lxml")
        return page_content

    @staticmethod
    def get_cache_dir():
        """

        :return:
        """
        return Path.home() / config.CACHE_DIR

    @staticmethod
    def url_hash(url):
        """

        :param url:
        :return:
        """
        return hashlib.md5(url.encode('utf8')).hexdigest()

    def save_cache(self, url, page_source):
        """

        :param url:
        :param page_source:
        :return:
        """
        cache_dir = self.get_cache_dir()
        cache_file = self.url_hash(url)
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with (cache_dir / cache_file).open('wb') as file:
            file.write(page_source)

    def get_cache(self, url):
        """

        :param url:
        :return:
        """
        cache = b''
        cache_dir = self.get_cache_dir()
        cache_file = self.url_hash(url)
        if (cache_dir / cache_file).exists():
            with (cache_dir / cache_file).open('rb') as file:
                cache = file.read()
        return cache

    def cache_lifetime(self, url):
        """

        :param url:
        :return:
        """
        cash_file_path = self.get_cache_dir() / self.url_hash(url)
        return time.time() - cash_file_path.stat().st_mtime < config.TIME_CACHE

    def weather_source(self, input_name):
        """

        :param input_name:
        :return:
        """
        weather_site = config.WEATHER_SITE
        if os.path.exists(self.get_settings_file()):
            weather_site = {self.get_settings()[2]: (self.get_settings()[1],
                                                     # URL це значення 'link' із файла конфігурації
                                                     *weather_site[self.get_settings()[2]][1:])
                            }
        if input_name:
            weather_site = {input_name: weather_site[input_name]}
        return weather_site

    @staticmethod
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

    @staticmethod
    def get_settings_file():
        """

        :return:
        """
        return str(Path.home() / config.CONFIG_FILE)

    def save_settings(self, name, url, site_set):
        """

        :param name:
        :param url:
        :param site_set:
        :return:
        """
        settings = configparser.RawConfigParser()  # якшо значення конфігурації
        # зчитувати за допомогою ConfigParser,це  робить неможливим використання "%".
        # Використано RawConfigParser, щоб уникнути спеціальної обробки значень конфігурації
        settings.add_section('SELECTED_LOCATION')
        settings.set('SELECTED_LOCATION', 'shortcut', site_set)
        settings.set('SELECTED_LOCATION', 'name', name)
        settings.set('SELECTED_LOCATION', 'link', url)
        settings.write(open(self.get_settings_file(), 'w', encoding='utf8'))

    def get_settings(self):
        """

        :return
        """
        settings = configparser.RawConfigParser()  # якшо значення конфігурації
        # зчитувати за допомогою ConfigParser,це  робить неможливим використання "%".
        # Використано RawConfigParser, щоб уникнути спеціальної обробки значень конфігурації
        settings.read(self.get_settings_file(), encoding='utf8')
        name = settings.get('SELECTED_LOCATION', 'name')
        url = settings.get('SELECTED_LOCATION', 'link')
        site_set = settings.get('SELECTED_LOCATION', 'shortcut')
        return name, url, site_set

    def clear_cache(self):
        """

        :return:
        """
        cache_dir = self.get_cache_dir()
        if cache_dir.exists():
            for file in os.listdir(str(cache_dir)):
                if time.time() - (cache_dir / file).stat().st_mtime > config.TIME_CACHE:
                    os.remove(str(cache_dir / file))


class AccuWeatherProvider(WeatherProvider):
    """
    Accuweather.com
    """
    shortcut = config.ACCU_SHORTCUT
    title = config.ACCU_TITLE
    input_name = shortcut

    def __init__(self):
        super().__init__(self)

        name, url = self.create_settings(site_set=None, refresh=False)
        self.name = name
        self.url = url

    def create_settings(self, site_set, refresh):
        """

        :param site_set:
        :param refresh:
        :return:
        """
        name = config.CITY
        link = config.ACCU_URL
        if not site_set:
            return name, link
        link_set, locations_list, location_name, location_link = \
            config.ACCU_SET, config.ACCU_LIST, config.ACCU_NAME, config.ACCU_LINK
        content = self.get_page_content(link_set, refresh)

        while content:
            search_list = []
            search_content = content.find_all(locations_list[0][0], locations_list[0][1])

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
                content = self.get_page_content(search_list[select][1], refresh)
                link = search_list[select][1]
                name = search_list[select][0]
            else:
                break

        self.save_settings(name, link, site_set)


class Rp5WeatherProvider(WeatherProvider):
    """
    RP5.ua
    """
    shortcut = config.RP5_SHORTCUT
    title = config.RP5_TITLE
    input_name = shortcut

    def __init__(self):
        super().__init__(self)

        name, url = self.create_settings(site_set=None, refresh=False)
        self.name = name
        self.url = url

    def create_settings(self, site_set, refresh):
        """

        :param site_set:
        :param refresh:
        :return:
        """
        name = config.CITY
        link = config.RP5_URL
        if not site_set:
            return name, link
        link_set, locations_list, location_name, location_link = \
            config.RP5_SET, config.RP5_LIST, config.RP5_NAME, config.RP5_LINK
        content = self.get_page_content(link_set, refresh)
        dom = htmldom.HtmlDom(link_set)
        dom = dom.createDom()

        while content:
            search_list = []
            if len(locations_list) == 1:
                search_content = content.find_all(locations_list[0][0], locations_list[0][1])
                if not search_content:
                    search_content = content.find_all(config.RP5_VAR[0], config.RP5_VAR[1])
                    # для деяких кінцевих сторінок з RP5, які мають іншу структуру тегів
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
                content = self.get_page_content(
                    dom.baseURL + '/' +
                    quote(search_list[select][1], encoding='utf8'), refresh)
                link = dom.baseURL + '/' + quote(search_list[select][1])
                name = search_list[select][0]
            else:
                break

        self.save_settings(name, link, site_set)
