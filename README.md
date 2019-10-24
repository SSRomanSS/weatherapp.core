# **WeatherApp Project**
### This is a Python console application that aggregates weather forecast from two sites:
### *[accuweather.com](https://www.accuweather.com), [rp5.ua](https://rp5.ua)*
> By default, the application displays the weather forecast for Dnipro, Ukraine.
> You can configurate the city before use
<br />

## Installation
Download the repository and use the following command to locally install the package:
```
$ pip install .
```
## Commands
* get the weather data from all providers:
```
$ weather
```
* get a list of all providers:
```
$ weather -p, --providers
```
* get weather data from a specific provider:
```
$ weather [provider]
```
* configurate your location to get weather information:
```
$ weather -s, --settings [provider]
```
* reset to default settings:
```
$ weather -s, --settings [reset]
```
* get the weather data into a text file:
```
$ weather -fo, --file [output_file]
```
* update cache:
```
$ weather -r, --refresh
```
* see a full trancback for errors:
```
$ [command] -d, --debug
```
* for setting the login level of the program(default WARNING) INFO:
```
$ weather [command] -v
```
* for setting the login level of the program(default WARNING) DEBUG:
```
$ weather [command] -vv
```
* remove app:
```
$ pip uninstall weatherapp
```
