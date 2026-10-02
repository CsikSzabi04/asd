import atexit
import os
import subprocess
import sys
from flask import Flask, jsonify, render_template, request
import mysql.connector

ROOT = os.path.dirname(os.path.abspath(__file__))
WEB_PORT = 5173
API_PORT = 5000

app = Flask(__name__, static_folder='static', template_folder='templates')


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Forklift.2026",
        database="forklift"
    )

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/forklift/<int:forklift_id>')
def forklift(forklift_id):
    return render_template('terkep.html', forklift_id=forklift_id)


@app.route('/api/positions', methods=['GET'])
def get_positions():
    date = request.args.get("date")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    forklift_id = request.args.get("forklift_id")

    if not date or not forklift_id:
        return jsonify([])

    allowed_tables = {
        "1": "teszt1",
        "2": "teszt2",
        "3": "teszt3",
        "4": "teszt4",
        "5": "teszt5",
        "6": "teszt6",
    }

    table_name = allowed_tables.get(forklift_id)
    if not table_name:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT latitude AS lat, longitude AS lon, datum, time
        FROM {table_name}
        WHERE datum = %s
    """

    params = [date]

    if start_time and end_time:
        query += " AND time BETWEEN %s AND %s"
        params.extend([start_time, end_time])

    query += " ORDER BY time ASC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


if __name__ == '__main__':
    dev = "--no-web" not in sys.argv

    if dev:
        vite = subprocess.Popen(
            f"npm run dev -- --port {WEB_PORT} --strictPort", cwd=ROOT, shell=True
        )
        atexit.register(lambda: os.system(f"taskkill /F /T /PID {vite.pid} >nul 2>&1"))

    app.run(host="127.0.0.1", port=API_PORT, use_reloader=False)