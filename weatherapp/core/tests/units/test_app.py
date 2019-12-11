"""
Some unit tests for app
"""
import unittest
import argparse

from weatherapp.core.app import App


class AppTestCase(unittest.TestCase):
    """
    Test application class methods.
    """

    def setUp(self):
        self.parser = App._create_parser()

    def test_arg_parser(self):
        """
        Test application argument parser creation.
        """

        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_arg_parser_default_values(self):
        """
        Test application argument parser default values.
        """

        parsed_args = self.parser.parse_args([])
        self.assertIsNone(parsed_args.site)
        self.assertFalse(parsed_args.debug)
        self.assertFalse(parsed_args.refresh)
        self.assertIsNone(parsed_args.providers)
        self.assertEqual(parsed_args.formatter, 'table')
        self.assertEqual(parsed_args.log_level, 0)

    def test_arg_parser_arg(self):
        """
        Test application argument parser.
        """

        parsed_args = self.parser.parse_args(['accu', '--debug', '--refresh',
                                              '-v', '--providers'])

        self.assertEqual(parsed_args.site, 'accu')
        self.assertTrue(parsed_args.debug)
        self.assertEqual(parsed_args.formatter, 'table')
        self.assertTrue(parsed_args.refresh)
        self.assertEqual(parsed_args.log_level, 1)
        self.assertEqual(parsed_args.providers, 'providers')


if __name__ == '__main__':
    unittest.main()
