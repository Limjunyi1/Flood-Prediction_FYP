import datetime
from io import BytesIO
from flask import Flask, request, jsonify, send_file
from GetResult import GetResult # Import your prediction model implementation
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
getResult = GetResult()



@app.route('/predict', methods=['POST'])
def predict(): 
    data = request.json  # Assuming JSON data is sent in the request body
    city = data['city']  # Extract the city from the JSON data
    date = data['date']  # Extract the date from the JSON data
    prediction = getResult.get_prediction_result(city, date) # Call your prediction model function with city and date
    global result
    result = prediction[0][0]
    global shap_table
    shap_table = prediction[1]
    
    return jsonify(prediction[0])

@app.route('/graph', methods=['GET'])
def get_graph():
    graph = getResult.plot_shap_result(shap_table, result)

    # Generate a filename based on the current timestamp
    filename = "graph.png"

    # Return the graph data as a PNG file with a dynamic filename
    return send_file(
        graph,
        mimetype='image/png',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True)