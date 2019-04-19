"""
Some unit tests for providermanager
"""

import unittest

from weatherapp.core.providermanager import ProviderManager

class DummyProvider:
    pass

class ProviderManagerTestCase(unittest.TestCase):
    """
    Test case for ProviderManager
    """
    def setUp(self):
        self.provider_manager = ProviderManager()

    def test_add(self):
        """

        :return:
        """
        self.provider_manager.add('dummy', DummyProvider)

        self.assertTrue('dummy' in self.provider_manager._providers)
        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)

    def test_get(self):
        """

        :return:
        """
        self.provider_manager.add('dummy', DummyProvider)

        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)
        self.assertIsNone(self.provider_manager.get('any'))

    def test_contains(self):
        """

        :return:
        """
        self.provider_manager.add('dummy', DummyProvider)

        self.assertTrue('dummy' in self.provider_manager)
        self.assertFalse('any' in self.provider_manager)

    def test_iter(self):
        """

        :return:
        """
        self.provider_manager.add('dummy', DummyProvider)

        for name in self.provider_manager:
            self.assertTrue(name in self.provider_manager)


if __name__ == '__main__':
    unittest.main()
