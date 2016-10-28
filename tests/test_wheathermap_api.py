import json
import os
import random
from configparser import ConfigParser
from random import randint
import json
from jsonschema import validate

import unittest2
import requests


class TestWeathermapApi(unittest2.TestCase):

    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={query}&units={units}"

    @classmethod
    def setUpClass(cls):
        config = ConfigParser()
        config_dir = os.path.dirname(__file__)
        config.read(os.path.join(config_dir, 'TESTS.ini'))
        cls.headers = {"X-API-KEY": config.get("KEYS", "API_KEY")}

    def setUp(self):
        pass

    def test_get_current_weather_by_city_and_country(self):
        url = self.WEATHER_URL.format(query="berlin, de", units="metric")
        weather = requests.get(url, headers=self.headers).json()
        self.assertEqual(weather['name'].lower(), 'berlin')
        self.assertIsNotNone(weather['weather'])

    def test_get_current_weather_by_city_name(self):
        url = self.WEATHER_URL.format(query="cordoba", units="metric")
        weather = requests.get(url, headers=self.headers).json()
        self.assertEqual(weather['name'].lower(), 'cordoba')
        self.assertIsNotNone(weather['weather'])

    def test_get_current_weather_by_city_id(self):
        url = self.WEATHER_URL.format(query="id=3860259", units="metric")
        weather = requests.get(url, headers=self.headers).json()
        self.assertEqual(weather['name'].lower(), 'pecenongan')
        self.assertIsNotNone(weather['weather'])

    def test_invalid_city_return_valid_error(self):
        url = self.WEATHER_URL.format(query="not_existed", units="metric")
        weather = requests.get(url, headers=self.headers).json()
        self.assertEqual(weather['cod'], '502')
        self.assertEqual(weather['message', 'Error: Not found city'])

    def test_invalid_country_return_valid_error(self):
        url = self.WEATHER_URL.format(query="cordoba, invalid_country", units="metric")
        weather = requests.get(url, headers=self.headers).json()
        self.assertEqual(weather['name'].lower(), 'monteria')
        self.assertIsNotNone(weather['weather'])

    def test_valid_data_return_for_multiple_cities(self):
        cities_file = os.path.join(os.path.dirname(__file__), "cities.json")
        with open(cities_file) as cities_by_country:
            data = json.load(cities_by_country)
        countries = random.sample(list(data), 10)
        for country in countries:
            max_cities = len(data[country]) - 1
            random_city = randint(0, max_cities)
            url = self.WEATHER_URL.format(query=data[country][random_city], units="metric")
            weather = requests.get(url, headers=self.headers).json()
            self.assertEqual(weather['name'].lower(), data[country][random_city].lower())
            self.assertIsNotNone(weather['weather'])

    def test_invalid_celcius_farenheit_convertion(self):
        url = self.WEATHER_URL.format(query="cordoba, ar", units="metric")
        weather_celcius = requests.get(url, headers=self.headers).json()
        url = self.WEATHER_URL.format(query="cordoba, ar", units="imperial")
        weather_farenheit = requests.get(url, headers=self.headers).json()
        self.assertEqual(round(abs(weather_farenheit['main']['temp'] -
                             self._celcius_to_farenheit(weather_celcius['main']['temp'])), 1)
                         , 0)

    def test_validate_weather_schema(self):
        schema_file = os.path.join(os.path.dirname(__file__), "weather_schema.json")
        with open(schema_file) as schema_json:
            schema = json.load(schema_json)
        url = self.WEATHER_URL.format(query="berlin, de", units="metric")
        weather = requests.get(url, headers=self.headers).json()
        validate(weather, schema)

    def _celcius_to_farenheit(self, celcius_temp):
        return round((celcius_temp * 9 / 5) + 32, 2)