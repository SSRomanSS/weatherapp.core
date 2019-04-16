from setuptools import find_namespace_packages, setup

setup(
    name="weatherapp",
    version="0.1.0",
    author="Roman S",
    description="A simple weather aggregator",
    long_descriptoin="",
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': 'weather=weatherapp.core.app:main'
    },
    install_requires=[
        'requests',
        'bs4',
        'htmldom',
        'prettytable'
        ]
    )
