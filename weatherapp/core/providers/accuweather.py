# -*- coding: utf-8 -*-
"""
accuweather provider
"""
import sys
import re

from weatherapp.core import config
from weatherapp.core.abstract import WeatherProvider


class AccuWeatherProvider(WeatherProvider):
    """
    Accuweather.com
    """
    title = config.ACCU_TITLE
    provider_name = config.ACCU_SHORTCUT
    city = config.CITY
    url = config.ACCU_URL

    def create_default_settings(self):
        """

        :return:
        """
        city = self.city
        url = self.url
        provider_name = self.provider_name
        self.save_settings(city, url, provider_name)

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

    def get_weather_info(self, page_content):
        """ Get weather information.
        """

        current_day_section = page_content.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {'Conditions': '-', 'Temperature': '-', 'Feels like': '-', 'Wind': '-'}
        if current_day_section:
            current_day_url = current_day_section.find('a').attrs['href']
            if current_day_url:
                current_day = self.get_page_content(current_day_url)
                if current_day:
                    weather_details = \
                        current_day.find('div', attrs={'id': 'detail-now'})
                    condition = weather_details.find('span', class_='cond')
                    if condition:
                        weather_info['Conditions'] = condition.text
                    temp = weather_details.find('span', class_='large-temp')
                    if temp:
                        weather_info['Temperature'] = temp.text
                    feal_temp = weather_details.find('span',
                                                     class_='small-temp')
                    if feal_temp:
                        weather_info['Feels like'] = feal_temp.text

                    wind_info = weather_details.find_all('li', class_='wind')
                    if wind_info:
                        weather_info['Wind'] = \
                            ' '.join(map(lambda t: t.text.strip(), wind_info))

        return weather_info
