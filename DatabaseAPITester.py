import unittest
import requests
import json

class TestGetData(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:8000'  # Replace with your actual server URL

    def test_get_data(self):
        # Define the data to send
        data = {
            'city': 'Dhaka',
            'year': '2024',
            'month': '5',
            'day': None
        }

        # Send a POST request to the /get_data endpoint
        response = requests.post(f'{self.BASE_URL}/get_data', json=data)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the response is JSON
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # Parse the JSON response
        response_data = response.json()

        # Check that the response data is as expected
        # This will depend on what your function is supposed to return
        # Here's an example:
        print(response_data)

if __name__ == '__main__':
    unittest.main()
