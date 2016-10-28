from configparser import ConfigParser

import unittest2
import requests


class TestWeathermapApi(unittest2.TestCase):

    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={units}"

    @classmethod
    def setUpClass(cls):
        config = ConfigParser()
        config.read('TESTS.ini')
        cls.headers = {"X-API-KEY": config.get("KEYS", "API_KEY")}

    def setUp(self):
        pass

    def test_get_current_weather_by_city_and_country(self):
        url = self.WEATHER_URL.format(city="berlin", country="de", units="metric")
        weather = requests.get(url, headers=self.headers).json()
        self.assertEquals(weather['name'].lower(), 'berlin')
        self.assertIsNotNone(weather['weather'])

