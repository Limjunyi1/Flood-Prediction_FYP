import requests

# Define the URL of your Flask API endpoint
url = 'http://127.0.0.1:5000/predict'

# Define the input data (city and date)
data = {
    'city': 'Dhaka',  # Replace 'YourCity' with the actual city name
    'date': '2024-05-03'  # Replace 'YYYY-MM-DD' with the actual date
}

# Send a POST request to the Flask API endpoint
response = requests.post(url, json=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the predicted result
    print('Prediction Result:', response.json())
else:
    # Print an error message if the request was not successful
    print('Error:', response.text)