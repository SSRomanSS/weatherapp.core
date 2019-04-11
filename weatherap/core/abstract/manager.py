"""

"""

import abc


class Manager(abc.ABC):

    """
    Abstract class for project command managers.
    """

    @abc.abstractmethod
    def add(self, name, command):
        """

        :param name:
        :param command:
        :return:
        """

    @abc.abstractmethod
    def get(self, name):
        """

        :param name:
        :return:
        """

    @abc.abstractmethod
    def __getitem__(self, name):
        """

        :param name:
        :return:
        """

    @abc.abstractmethod
    def __contains__(self, name):
        """

        :param name:
        :return:
        """
