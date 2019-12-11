# -*- coding: utf-8 -*-
"""
Container of provider
"""
from weatherapp.core.providers import AccuWeatherProvider, Rp5WeatherProvider
from weatherapp.core import abstract


class ProviderManager(abstract.Manager):
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
            self.add(provider.provider_name, provider)

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

    def __getitem__(self, name):
        """

        :param name:
        :return:
        """
        return self._providers[name]

    def __iter__(self):
        """

        :return:
        """
        for key in self._providers:
            yield key
