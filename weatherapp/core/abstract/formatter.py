import abc


class Formatter(abc.ABC):

    """
    Base abstract class for formatters.
    """

    @abc.abstractmethod
    def output_format(self, data):
        """

        :param data:
        :return:
        """