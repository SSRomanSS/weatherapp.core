# -*- coding: utf-8 -*-
"""
This is weather search script
"""
import argparse
import html
import os
import sys


from weatherap.core import config
import logging
from weatherap.core.providermanager import ProviderManager
from weatherap.core.commandmanager import CommandManager
from weatherap.core.abstract import WeatherProvider


class App:
    """
    Main application
    """
    logger = logging.getLogger()
    LOG_LEVEL = {0: logging.WARNING,
                 1: logging.INFO,
                 2: logging.DEBUG}

    def __init__(self):
        self.provider_manager = ProviderManager()
        self.command_manager = CommandManager()
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
        parser.add_argument('-p', '--providers',
                            help='Output available providers ',
                            action='store_const',
                            const='providers')
        parser.add_argument('-d', '--debug', help='Develop mode', action='store_true')
        parser.add_argument('-v', '--verbose', action='count', dest='log_level', default=0)
        return parser

    def configure_logger(self):
        """

        :return:
        """
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console_level = self.LOG_LEVEL.get(self.commands.log_level)
        console.setLevel(console_level)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        console.setFormatter(formatter)
        root_logger.addHandler(console)

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
        WeatherProvider(App()).clear_cache()
        self.configure_logger()
        provider_box = self.provider_manager._providers

        if self.commands.site is not None and self.commands.site not in provider_box\
                and self.commands.settings not in provider_box:
            sys.exit('Unknown command')

        if self.commands.settings == 'reset' and \
                os.path.exists(WeatherProvider(App()).get_settings_file()):
            os.remove(WeatherProvider(App()).get_settings_file())  # removing settings file

        if not os.path.exists(WeatherProvider(App()).get_settings_file()):
            for provider in provider_box:
                provider_box[provider](App).create_default_settings()
                # create file with default settings
        if self.commands.providers:
            print('Available providers:')
            sys.exit(self.command_manager.get(self.commands.providers)(App()).run())

        if self.commands.settings in provider_box:
            self.command_manager.get('settings')(App()).run(self.commands.settings)
            # create settings for selected provider

        if self.commands.site in provider_box:
            configured_provider_box = {self.commands.site: provider_box[self.commands.site]}
        else:
            configured_provider_box = provider_box

        for name in configured_provider_box:
            self.result_output(name,
                               *WeatherProvider(App()).run(name),
                               provider_box[name](App)
                               )


def main():
    """

    :return:
    """
    return App().run()


if __name__ == '__main__':
    main()
