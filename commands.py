"""
App commands
"""
import re
from abstract import Command


class Configurate(Command):
    """
    Configure provider
    """
    name = 'settings'

    def run(self, provider_name):
        """
        Run command
        """
        provider = self.app.provider_manager.get(provider_name)
        provider(self.app).create_settings(provider_name)


class Providers(Command):
    """
    List of providers
    """
    name = 'providers'

    def run(self):
        """
        Run command
        """
        providers = self.app.provider_manager._providers
        for name in providers:
            print('{} - "{}"'.format(name, providers.get(name).title))
