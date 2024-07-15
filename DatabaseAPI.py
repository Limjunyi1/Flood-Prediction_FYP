from collections import OrderedDict
import datetime
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

# MySQL configurations
db_config = {
    'host': 'flood-prediction-fyp.mysql.database.azure.com',
    'user': 'jlim0199',
    'password': os.environ.get('DB_PASSWORD'),
    'database': 'flood_data',
}

# Check if password is None
if db_config['password'] is None:
    raise ValueError("Please set up DB_PASSWORD environment variable in your system !!!")

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


@app.route('/get_data', methods=['POST'])
def get_data():
    try:
        data = request.json
        print(data)
        city = data['city']
        year = data['year']
        month = data['month']
        day = data['day']

        print(city, year, month, day)

        cursor = conn.cursor()
        if not city and not day and not month and not year:
            cursor.execute("SELECT * FROM PREDICTION_RESULT")
            data = [list(row) for row in cursor.fetchall()]
            cursor.close()
            return jsonify(data)
        elif not city:
            if not day and not year:
                query = "SELECT * FROM PREDICTION_RESULT WHERE Month = %s"
                values = (month,)
            elif not day and not month:
                query = "SELECT * FROM PREDICTION_RESULT WHERE Year = %s"
                values = (year,)
            elif not day:
                query = "SELECT * FROM PREDICTION_RESULT WHERE Year = %s AND Month = %s"
                values = (year, month)
            else:
                query = "SELECT * FROM PREDICTION_RESULT WHERE Year = %s AND Month = %s AND Day = %s"
                values = (year, month, day)
        else:
            if not day and not month and not year:
                query = "SELECT * FROM PREDICTION_RESULT WHERE City = %s"
                values = (city,)
            elif not day and not year:
                query = "SELECT * FROM PREDICTION_RESULT WHERE City = %s AND Month = %s"
                values = (city, month)
            elif not day and not month:
                query = "SELECT * FROM PREDICTION_RESULT WHERE City = %s AND Year = %s"
                values = (city, year)
            elif not day:
                query = "SELECT * FROM PREDICTION_RESULT WHERE City = %s AND Year = %s AND Month = %s"
                values = (city, year, month)
            else:
                query = "SELECT * FROM PREDICTION_RESULT WHERE City = %s AND Year = %s AND Month = %s AND Day = %s"
                values = (city, year, month, day)
        cursor.execute(query, values)
        data = [list(row) for row in cursor.fetchall()]
        cursor.close()

        print(data)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True, port=8000)