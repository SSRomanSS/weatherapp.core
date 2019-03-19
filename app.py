# -*- coding: utf-8 -*-
"""
This is weather search script
"""
import argparse
import html
import os
import sys

import config
import providers
from providermanager import ProviderManager


class App:
    """

    """

    def __init__(self):
        self.parser = self._create_parser()
        self.provider_manager = ProviderManager()

    @staticmethod
    def _create_parser():
        """
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('site', help='Choice website: '
                                         'accu=Accuwether, '
                                         'rp5=RP5.ua',
                            nargs='?', default='')
        parser.add_argument('-f', '--file', help='The name of file for output',
                            type=argparse.FileType(mode='w', encoding='utf8'))
        parser.add_argument('-s', '--settings', nargs='?')
        parser.add_argument('-r', '--refresh', help='Refresh cache', action='store_true')
        return parser

    @staticmethod
    def result_output(website, temperature, conditions, provider):
        """
        :param website:
        :param temperature:
        :param conditions:
        :param provider
        :return:
        """
        if os.path.exists(provider.get_settings_file()):
            print(provider.get_settings()[0])
            print('=' * 20)
        else:
            print(config.CITY)
            print('=' * 20)
        print('From {}:'.format(website))
        print('-' * 20)
        print('Temperature: {}'
              .format(html.unescape(temperature.replace(' ', ''))))
        print('Weather conditions:' + '\n{}\n'
              .format(conditions.strip()).replace(', ', '\n'))

    @staticmethod
    def file_output(result, out_file, provider):
        """
        :param result:
        :param out_file:
        :param provider:
        :return:
        """

        for name in result:
            if os.path.exists(provider.get_settings_file()):
                print(provider.get_settings()[0], '\n',
                      '=' * 20, '\n', file=out_file)
            else:
                print(config.CITY, '\n',
                      '=' * 20, '\n', file=out_file)
            print('From {}:\n'.format(name),
                  '-' * 20, '\n',
                  'Temperature: {}\n'.format(html.unescape(result[name][0].replace(' ', ''))),
                  'Weather conditions:\n {}\n'.format(result[name][1].strip().replace(', ', '\n')),
                  file=out_file)
        out_file.close()

    def run(self):
        """
        :return:
        """
        providers.WeatherProvider(app=True).clear_cache()
        provider_box = self.provider_manager._providers

        input_name = self.parser.parse_args(sys.argv[1:]).site
        out_file = self.parser.parse_args(sys.argv[1:]).file
        site_set = self.parser.parse_args(sys.argv[1:]).settings
        refresh = self.parser.parse_args(sys.argv[1:]).refresh

        if input_name not in provider_box and input_name != '' and site_set not in provider_box:
            sys.exit('Unknown command')
        if input_name != '' and \
                os.path.exists(providers.WeatherProvider(app=True).get_settings_file()):
            sys.exit('Reset the settings: [-s] reset')
        if site_set == 'reset' and \
                os.path.exists(providers.WeatherProvider(app=True).get_settings_file()):
            os.remove(providers.WeatherProvider(app=True).get_settings_file())
        if site_set in provider_box and site_set != 'reset':
            provider_box[site_set]().create_settings(site_set, refresh)

        out_dict = {}
        if site_set in provider_box:
            provider_box = {site_set: provider_box[site_set]}
        if input_name in provider_box:
            provider_box = {input_name: provider_box[input_name]}
        if os.path.exists(providers.AccuWeatherProvider().get_settings_file()):
            provider_box = {providers.WeatherProvider(app=True).get_settings()[2]:
                            provider_box[providers.WeatherProvider(app=True).get_settings()[2]]
                            }

        for name in provider_box:
            url, temp_tags, cond_tags = provider_box[name]().weather_source(input_name)[name]
            page_content = provider_box[name]().get_page_content(url, refresh)
            temperature = provider_box[name]().get_weather_info(page_content, temp_tags)
            conditions = provider_box[name]().get_weather_info(page_content, cond_tags)
            self.result_output(name, temperature, conditions, provider_box[name]())
            if out_file:
                out_dict[name] = (temperature, conditions)
        if out_file:
            self.file_output(out_dict, out_file, providers.WeatherProvider(app=True))


def main():
    """

    :return:
    """
    return App().run()


if __name__ == '__main__':
    main()
