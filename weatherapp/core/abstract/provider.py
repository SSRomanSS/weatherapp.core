"""
Abstract classes for project
"""

import os
import sys
import time
from pathlib import Path
import urllib.error
from urllib.request import urlopen, Request
import configparser
import hashlib
from bs4 import BeautifulSoup



from weatherapp.core import config
from weatherapp.core.abstract.command import Command


class WeatherProvider(Command):
    """
    Common WeatherProvider
    """
    def __init__(self, app):
        """

        :param app
        """
        super().__init__(app)

    def get_page_content(self, url):
        """

        :param url:
        :return:
        """
        if self.get_cache(url) and self.cache_lifetime(url) and not self.app.commands.refresh:
            content = self.get_cache(url)
        else:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            request = Request(url, headers=headers)
            try:
                content = urlopen(request).read()  # if url is damaged
            except urllib.error.URLError:
                msg = 'Bad configfile, use --reset'
                if self.app.commands.debug:
                    self.app.logger.exception(msg)
                else:
                    self.app.logger.error(msg)
                sys.exit()
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

    @staticmethod
    def get_settings_file():
        """

        :return:
        """
        return str(Path.home() / config.CONFIG_FILE)

    def save_settings(self, city, url, provider_name):
        """

        :param city:
        :param url:
        :param provider_name:
        :return:
        """
        settings = configparser.RawConfigParser()
        # Configuration values were read using ConfigParser,
        # which does string interpolation, for instance making it impossible to use "%".
        # Switches to RawConfigParser to avoid any special treatment of configuration values

        settings.read(self.get_settings_file(), encoding='utf8')
        settings.sections()
        if settings.has_section(provider_name):
            settings.remove_section(provider_name)
        settings.add_section(provider_name)
        settings.set(provider_name, 'shortcut', provider_name)
        settings.set(provider_name, 'city', city)
        settings.set(provider_name, 'url', url)
        with open(self.get_settings_file(), 'w', encoding='utf8') as file:
            settings.write(file)

    def get_settings(self, provider_name):
        """

        :return
        """
        settings = configparser.RawConfigParser()
        # Configuration values were read using ConfigParser,
        # which does string interpolation, for instance making it impossible to use "%".
        # Switches to RawConfigParser to avoid any special treatment of configuration values
        open(self.get_settings_file(), 'r+')
        try:
            settings.read(self.get_settings_file(), encoding='utf8')  # if configfile is damaged
        except configparser.Error:
            msg = 'Bad configfile, use --reset'
            if self.app.commands.debug:
                self.app.logger.exception(msg)
            else:
                self.app.logger.error(msg)
            sys.exit()
        city = settings.get(provider_name, 'city')
        url = settings.get(provider_name, 'url')
        provider_name = settings.get(provider_name, 'shortcut')
        return city, url, provider_name

    def clear_cache(self):
        """

        :return:
        """
        cache_dir = self.get_cache_dir()
        if cache_dir.exists():
            for file in os.listdir(str(cache_dir)):
                if time.time() - (cache_dir / file).stat().st_mtime > config.TIME_CACHE:
                    os.remove(str(cache_dir / file))

    def run(self, provider_name):
        """

        :param provider_name:
        :return:
        """
        summary_info = {}

        providers = self.app.provider_manager
        url = self.get_settings(provider_name)[1]
        page_content = self.get_page_content(url)
        weather_info = providers[provider_name](self.app).get_weather_info(page_content)
        summary_info['City'] = self.get_settings(provider_name)[0]
        summary_info['Provider'] = providers[provider_name].title
        for key in weather_info:
            summary_info[key] = weather_info[key]
        return summary_info
