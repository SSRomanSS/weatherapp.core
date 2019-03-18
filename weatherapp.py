# -*- coding: utf-8 -*-
"""
This is weather search script
"""
import sys
import argparse
import html
import os
import providers
import config


def create_parser():
    """
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('site', help='Choice website: '
                                     'accu=Accuwether, '
                                     'rp5=RP5.ua, '
                                     'sin=sinoptik.ua',
                        nargs='?', default='')
    parser.add_argument('-f', '--file', help='The name of file for output',
                        type=argparse.FileType(mode='w', encoding='utf8'))
    parser.add_argument('-s', '--settings', nargs='?')
    parser.add_argument('-r', '--refresh', help='Refresh cache', action='store_true')
    return parser


def result_output(website, temperature, conditions, provider):
    """
    :param website:
    :param temperature:
    :param conditions:
    :param provider
    :return:
    """
    if os.path.exists(provider.get_settings_file()):
        print(provider.get_settings()[0])
    else:
        print(config.CITY)
    print('From {}:'.format(website))
    print('Temperature: {}'
          .format(html.unescape(temperature.replace(' ', ''))))
    print('Weather conditions:' +'\n{}\n'
          .format(conditions.strip()).replace(', ', '\n'))


def file_output(result, out_file, provider):
    """
    :param result:
    :param out_file:
    :param provider:
    :return:
    """

    for name in result:
        if os.path.exists(provider.get_settings_file()):
            print(provider.get_settings()[0], file=out_file)
        else:
            print(config.CITY, file=out_file)
        print('From {}:\n'.format(name),
              'Temperature: {}\n'.format(html.unescape(result[name][0].replace(' ', ''))),
              'Weather conditions:\n {}\n'.format(result[name][1].strip().replace(', ', '\n')),
              file=out_file)
    out_file.close()


def main():
    """
    :return:
    """
    providers.AccuWeatherProvider().clear_cache()
    known_command = {'accu': providers.AccuWeatherProvider(),
                     'rp5': providers.Rp5WeatherProvider()
                     }

    input_name = create_parser().parse_args(sys.argv[1:]).site
    out_file = create_parser().parse_args(sys.argv[1:]).file
    site_set = create_parser().parse_args(sys.argv[1:]).settings
    refresh = create_parser().parse_args(sys.argv[1:]).refresh
    if input_name not in known_command and input_name != '' and site_set not in known_command:
        sys.exit('Unknown command')
    if input_name and os.path.exists(known_command[input_name].get_settings_file()):
        sys.exit('Reset the settings: [-s] reset')
    if site_set == 'reset' and os.path.exists(providers.AccuWeatherProvider().get_settings_file()):
        os.remove(providers.AccuWeatherProvider().get_settings_file())
    if site_set in known_command and site_set != 'reset':
        known_command[site_set].create_settings(site_set, refresh)

    out_dict = {}
    if site_set in known_command:
        known_command = {site_set: known_command[site_set]}
    if input_name in known_command:
        known_command = {input_name: known_command[input_name]}
    if os.path.exists(providers.AccuWeatherProvider().get_settings_file()):
        known_command = {providers.AccuWeatherProvider().get_settings()[2]:
                         known_command[providers.AccuWeatherProvider().get_settings()[2]]
                         }

    for name in known_command:
        url, temp_tags, cond_tags = known_command[name].weather_source(input_name)[name]
        page_content = known_command[name].get_page_content(url, refresh)
        temperature = known_command[name].get_weather_info(page_content, temp_tags)
        conditions = known_command[name].get_weather_info(page_content, cond_tags)
        result_output(name, temperature, conditions, known_command[name])
        if out_file:
            out_dict[name] = (temperature, conditions)
    if out_file:
        file_output(out_dict, out_file, providers.AccuWeatherProvider())


if __name__ == '__main__':
    main()
    