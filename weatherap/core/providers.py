# -*- coding: utf-8 -*-
"""
Weather providers
"""
import sys
from urllib.parse import quote
from htmldom import htmldom

from weatherap.core import config
from weatherap.core.abstract import WeatherProvider


class AccuWeatherProvider(WeatherProvider):
    """
    Accuweather.com
    """
    shortcut = config.ACCU_SHORTCUT
    title = config.ACCU_TITLE
    provider_name = shortcut
    city = config.CITY
    url = config.ACCU_URL

    def create_default_settings(self):
        """

        :return:
        """
        city = self.city
        url = self.url
        shortcut = self.shortcut
        self.save_settings(city, url, shortcut)

    def create_settings(self, provider_name):
        """

        :param provider_name:
        :return:
        """

        city = ''
        url = ''
        link_set, locations_list, location_name, location_link = \
            config.ACCU_SET, config.ACCU_LIST, config.ACCU_NAME, config.ACCU_LINK
        content = self.get_page_content(link_set)

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
                    msg = 'You input not number. Restart'
                    if self.app.commands.debug:
                        self.app.logger.exception(msg)
                    else:
                        self.app.logger.error(msg)
                    sys.exit()
                try:
                    content = self.get_page_content(search_list[select][1])
                except IndexError:
                    msg = 'Selected number is not in list'
                    if self.app.commands.debug:
                        self.app.logger.exception(msg)
                    else:
                        self.app.logger.error(msg)
                    sys.exit()
                url = search_list[select][1]
                city = search_list[select][0]
            else:
                break
        self.save_settings(city, url, provider_name)


class Rp5WeatherProvider(WeatherProvider):
    """
    RP5.ua
    """
    shortcut = config.RP5_SHORTCUT
    title = config.RP5_TITLE
    provider_name = shortcut
    city = config.CITY
    url = config.RP5_URL

    def create_default_settings(self):
        """

        :return:
        """
        city = self.city
        url = self.url
        shortcut = self.shortcut
        self.save_settings(city, url, shortcut)

    def create_settings(self, provider_name):
        """

        :param provider_name:
        :return:
        """

        city = ''
        url = ''
        link_set, locations_list, location_name, location_link = \
            config.RP5_SET, config.RP5_LIST, config.RP5_NAME, config.RP5_LINK
        content = self.get_page_content(link_set)
        dom = htmldom.HtmlDom(link_set)
        dom = dom.createDom()

        while content:
            search_list = []
            if len(locations_list) == 1:
                search_content = content.find_all(locations_list[0][0], locations_list[0][1])
                if not search_content:
                    search_content = content.find_all(config.RP5_VAR[0], config.RP5_VAR[1])
                    # for some ending pages from RP5 that have a different tag structure
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
                    msg = 'You input not number. Restart'
                    if self.app.commands.debug:
                        self.app.logger.exception(msg)
                    else:
                        self.app.logger.error(msg)
                    sys.exit()
                try:
                    content = self.get_page_content(
                        dom.baseURL + '/' +
                        quote(search_list[select][1], encoding='utf8'))
                except IndexError:
                    msg = 'Selected number is not in list'
                    if self.app.commands.debug:
                        self.app.logger.exception(msg)
                    else:
                        self.app.logger.error(msg)
                    sys.exit()
                url = dom.baseURL + '/' + quote(search_list[select][1])
                city = search_list[select][0]
            else:
                break
        self.save_settings(city, url, provider_name)
