"""

"""
from commands import Configurate, Providers
import providermanager


class CommandManager(providermanager.ProviderManager):

    """ Discovers registered providers and loads them.
    """

    def _load_providers(self):
        """ Loads all existing providers.
        """

        for command in [Configurate, Providers]:
            self.add(command.name, command)
