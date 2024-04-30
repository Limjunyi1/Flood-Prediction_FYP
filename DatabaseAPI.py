from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)