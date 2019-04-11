"""

"""
from weatherap.core.abstract import Command


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
