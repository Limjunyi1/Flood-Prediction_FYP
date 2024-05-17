import requests
from PIL import Image
from io import BytesIO

# Define the URLs of your Flask API endpoints
predict_url = 'http://127.0.0.1:5000/predict'
graph_url = 'http://127.0.0.1:5000/graph'

# Define the input data (city and date)
data = {
    'city': 'Dhaka',
    'date': '2024-05-17'
}

# Send a POST request to the Flask API endpoint to get the prediction
response = requests.post(predict_url, json=data)

# Check if the prediction request was successful (status code 200)
if response.status_code == 200:
    # Print the predicted result
    prediction = response.json()
    print('Prediction Result:', prediction)

    # If the prediction was successful, fetch the SHAP graph
    graph_response = requests.get(graph_url)
    
    # Check if the graph request was successful (status code 200)
    if graph_response.status_code == 200:
        # Display the SHAP graph using PIL
        img = Image.open(BytesIO(graph_response.content))
        img.show()  # This will open the default image viewer and display the image
    else:
        # Print an error message if the graph request was not successful
        print('Error fetching graph:', graph_response.text)
else:
    # Print an error message if the prediction request was not successful
    print('Error fetching prediction:', response.text)
