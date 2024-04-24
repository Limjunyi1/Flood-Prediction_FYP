from flask import Flask, request, jsonify
from GetResult import GetResult # Import your prediction model implementation

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    getResult = GetResult()
    data = request.json  # Assuming JSON data is sent in the request body
    city = data['city']  # Extract the city from the JSON data
    date = data['date']  # Extract the date from the JSON data
    prediction = getResult.get_prediction_result(city, date) # Call your prediction model function with city and date
    
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)