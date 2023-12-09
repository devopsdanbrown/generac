import unittest
from unittest.mock import patch
from datetime import datetime
import nwsapi_dlbrown as nws

class TestNwsApi(unittest.TestCase):

    def test_check_valid_date(self):
        self.assertEqual(nws.check_valid_date('2023-12-01T00:00'), datetime(2023, 12, 1, 0, 0))
        self.assertIsNone(nws.check_valid_date('invalid-date'))

    @patch('builtins.input', return_value='12345')
    def test_get_zip_code(self, input):
        self.assertEqual(nws.get_zip_code(), '12345')

    @patch('builtins.input', side_effect=['invalid-date', '2023-12-01T00:00'])
    def test_get_start_date_time(self, input):
        self.assertEqual(nws.get_start_date_time(), datetime(2023, 12, 1, 0, 0))

    @patch('builtins.input', side_effect=['invalid-date', '2023-12-01T00:00'])
    def test_get_end_date_time(self, input):
        self.assertEqual(nws.get_end_date_time(), datetime(2023, 12, 1, 0, 0))

    # You may want to mock the requests.get call in the following two functions to avoid making actual HTTP requests in your tests.

if __name__ == '__main__':
    unittest.main()