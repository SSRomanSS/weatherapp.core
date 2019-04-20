"""
Some unit tests for provider
"""
import os
from pathlib import Path
import configparser
import unittest
import shutil


class WeatherProviderTestCase(unittest.TestCase):
    """
    Test case for WeatherProvider
    """
    def test_cache_handling(self):
        """
        Tests for get_cache_dir(), save_cache(), get_cache(), clear_cache()
        :return:
        """
        cache_dir = Path.home() / 'cache_dir'
        cache_file = 'cache_file'
        page_source = b'content'
        cache = b''
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)
        self.assertTrue(cache_dir / cache_file)

        with (cache_dir / cache_file).open('wb') as file:
            file.write(page_source)
        if (cache_dir / cache_file).exists():
            with (cache_dir / cache_file).open('rb') as file:
                cache = file.read()
        self.assertEqual(page_source, cache)

        if cache_dir.exists():
            os.remove(str(cache_dir / cache_file))
        self.assertFalse((cache_dir / cache_file).exists())

        shutil.rmtree(cache_dir)
        self.assertFalse(cache_dir.exists())

    def test_settings_handling(self):
        """
        Tests for get_settings_file(), save_settings(), get_settings()
        :return:
        """

        settings_file = 'test_settings.ini'
        settings = configparser.RawConfigParser()
        section = 'section'
        name = 'sample_name'

        settings.read(str(Path.home() / settings_file), encoding='utf8')
        settings.sections()
        if settings.has_section(section):
            settings.remove_section(section)
        settings.add_section(section)
        settings.set(section, 'name', name)

        with open(str(Path.home() / settings_file), 'w', encoding='utf8') as file:
            settings.write(file)

        self.assertTrue((Path.home() / settings_file).exists())

        with open(str(Path.home() / settings_file), 'r+', encoding='utf8') as file:
            settings.read(file)
        self.assertEqual(settings.get(section, 'name'), name)

        os.remove(str(Path.home() / settings_file))
        self.assertFalse((Path.home() / settings_file).exists())


if __name__ == '__main__':
    unittest.main()
