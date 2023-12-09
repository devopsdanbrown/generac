import unittest
from unittest.mock import patch
from datetime import datetime
import nwsapi_dlbrown as nws

class TestNwsApi(unittest.TestCase):

#write unit tests for each function in nwsapi_dlbrown.py
      
    def test_get_zip_code(self):
        # test that the function returns a string
        self.assertIsInstance(nws.get_zip_code(), str)
        # test that the string is 5 characters long
        self.assertEqual(len(nws.get_zip_code()), 5)
        # test that the string is all digits
        self.assertTrue(nws.get_zip_code().isdigit())
        
    def test_get_closest_weather_station(self):
        # test that the function returns a string
        self.assertIsInstance(nws.get_closest_weather_station(0, 0), str)
        # test that the string is 4 characters long
        self.assertEqual(len(nws.get_closest_weather_station(0, 0)), 4)
        # test that the string is all uppercase
        self.assertTrue(nws.get_closest_weather_station(0, 0).isupper())

    def test_fetch_historical_weather_observations(self):
        # test that the function returns a list
        self.assertIsInstance(nws.fetch_historical_weather_observations("KJFK"), list)
        # test that the list contains dictionaries
        self.assertIsInstance(nws.fetch_historical_weather_observations("KJFK")[0], dict)
        # test that the dictionary has the expected keys
        self.assertIn("properties", nws.fetch_historical_weather_observations("KJFK")[0])
        self.assertIn("timestamp", nws.fetch_historical_weather_observations("KJFK")[0])
        self.assertIn("temperature", nws.fetch_historical_weather_observations("KJFK")[0])
        self.assertIn("value", nws.fetch_historical_weather_observations("KJFK")[0])
        # test that the values are the expected data types
        self.assertIsInstance(nws.fetch_historical_weather_observations("KJFK")[0]["properties"], dict)
        self.assertIsInstance(nws.fetch_historical_weather_observations("KJFK")[0]["timestamp"], dict)
        self.assertIsInstance(nws.fetch_historical_weather_observations("KJFK")[0]["temperature"], str)
        self.assertIsInstance(nws.fetch_historical_weather_observations("KJFK")[0]["value"], str)

   
if __name__ == '__main__':
    unittest.main()
