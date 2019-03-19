# -*- coding: utf-8 -*-
"""

"""
from providers import AccuWeatherProvider, Rp5WeatherProvider


class ProviderManager:
    """
    Provider box
    """
    def __init__(self):
        """

        """
        self._providers = {}
        self._load_providers()

    def _load_providers(self):
        """

        :return:
        """
        for provider in [AccuWeatherProvider, Rp5WeatherProvider]:
            self.add(provider.shortcut, provider)

    def add(self, name, provider):
        """

        :param name:
        :param provider:
        :return:
        """
        self._providers[name] = provider

    def get(self, name):
        """

        :param name:
        :return:
        """
        return self._providers.get(name, None)

    def __len__(self):
        """

        :return:
        """
        return len(self._providers)

    def __contains__(self, name):
        """

        :param name:
        :return:
        """
        return name in self._providers

    def __getattr__(self, name):
        """

        :param name:
        :return:
        """
        return self._providers[name]
