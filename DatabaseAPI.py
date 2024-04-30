import datetime
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# MySQL configurations
db_config = {
    'host': 'flood-prediction-fyp.mysql.database.azure.com',
    'user': 'actp',
    'password': '!Q2w#E4r%T',
    'database': 'flood_data',
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)

@app.route('/database', methods=['GET'])
def index():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM BANGLADESH_FLOOD")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)


@app.route('/store', methods=['POST'])
def store():
    try:
        data = request.json
        city = data['city']
        date = data['date']
        year, month, day = map(int, date.split('-'))
        result = data['result']
        probability = float(data['probability'])
        prediction_made = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = conn.cursor()
        query = "INSERT INTO PREDICTION_RESULT (City, Year, Month, Day, Result, Probability, Prediction_Made) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (city, year, month, day, result, probability, prediction_made)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()

        return jsonify({'message': 'Data stored successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    


if __name__ == '__main__':
    app.run(debug=True, port=8000)