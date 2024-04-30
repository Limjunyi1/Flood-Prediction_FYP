import unittest
import requests

class TestAPI(unittest.TestCase):
    base_url = 'http://localhost:5000/database'  # Update with your API URL

    def test_get_data(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)  # Assuming your API returns a 200 status code for successful requests
        # Check that the response contains JSON data
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        # Verify the structure and content of the JSON response
        data = response.json()
        # Add assertions to check the structure and content of the data
        # For example, if you expect the data to be a list of dictionaries
        self.assertIsInstance(data, list)
        for item in data:
            print(item)
            # Add more specific assertions to check the content of each item if needed

if __name__ == '__main__':
    unittest.main()
