# -*- coding: utf-8 -*-
"""
This is weather search script
"""
import argparse
import html
import os
import sys

import config
from providermanager import ProviderManager
import abstract
from configurate import Configurate, Providers


class App:
    """
    Main application
    """
    def __init__(self):
        self.provider_manager = ProviderManager()
        self.commands = self._create_parser().parse_args(sys.argv[1:])

    @staticmethod
    def _create_parser():
        """
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('site', help='Choice website:'
                                         'accu=Accuwether,'
                                         'rp5=RP5.ua',
                            nargs='?', default=None)
        parser.add_argument('-f', '--file', help='The name of file for output',
                            type=argparse.FileType(mode='w', encoding='utf8'))
        parser.add_argument('-s', '--settings', help='Configure the providers with commands:'
                                                     '"accu" or "rp5". '
                                                     'Use command "reset" for default settings',
                            nargs='?')
        parser.add_argument('-r', '--refresh', help='Refresh cache', action='store_true')
        parser.add_argument('-l', '--list', help='Output available providers ', action='store_true')
        parser.add_argument('-d', '--debug', help='Develop mode', action='store_true')
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
            print(provider.get_settings(provider.shortcut)[0])
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

    def run(self):
        """
        :return:
        """
        abstract.WeatherProvider(App()).clear_cache()
        provider_box = self.provider_manager._providers

        if self.commands.site is not None and self.commands.site not in provider_box\
                and self.commands.settings not in provider_box:
            sys.exit('Unknown command')

        if self.commands.settings == 'reset' and \
                os.path.exists(abstract.WeatherProvider(App()).get_settings_file()):
            os.remove(abstract.WeatherProvider(App()).get_settings_file())  # removing settings file

        if not os.path.exists(abstract.WeatherProvider(App()).get_settings_file()):
            for provider in provider_box:
                provider_box[provider](App).create_default_settings()
                # create file with default settings
        if self.commands.list:
            print('Available providers:')
            sys.exit(Providers(App()).run())

        if self.commands.settings in provider_box:
            Configurate(App()).run(self.commands.settings)
            # create settings for selected provider

        if self.commands.site in provider_box:
            configured_provider_box = {self.commands.site: provider_box[self.commands.site]}
        else:
            configured_provider_box = provider_box

        for name in configured_provider_box:
            self.result_output(name,
                               *abstract.WeatherProvider(App()).run(name),
                               provider_box[name](App)
                               )


def main():
    """

    :return:
    """
    try:
        return App().run()
    except Exception:
        if App().commands.debug:
            raise
        sys.exit('Run error, contact with developer')


if __name__ == '__main__':
    main()
