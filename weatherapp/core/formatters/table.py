"""
Formatter for output in console
"""
import prettytable

from weatherapp.core.abstract import Formatter


class TableFormatter(Formatter):
    """
    Table formatter for app output.
    """

    def output_format(self, data):
        """

        :param data:
        :return:
        """

        table = prettytable.PrettyTable()
        table.field_names = ['TITLE', 'MEANING']
        for key in data:
            table.add_row([key, data[key]])

        return table.get_string()
