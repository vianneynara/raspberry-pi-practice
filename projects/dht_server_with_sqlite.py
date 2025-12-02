import board
import adafruit_dht
from flask import Flask
import datetime
import sqlite3
import threading
import time

# Initialize sensor
dht = adafruit_dht.DHT11(
    pin=board.D17,
    use_pulseio=False
)

app = Flask(__name__)
DB_NAME = 'temperature.db'


def init_db():
    """Membuat tabel database jika belum ada"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS temperature_log
              (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT NOT NULL,
                  temperature REAL NOT NULL,
                  humidity REAL NOT NULL
              )
              ''')
    conn.commit()
    conn.close()


def log_data_hourly():
    """Stores the data (temperature and humidity) every hour this method being executed."""
    while True:
        try:
            temp = dht.temperature
            hum = dht.humidity
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('INSERT INTO temperature_log (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                      (timestamp, temp, hum))
            conn.commit()
            conn.close()

            print(f"[{timestamp}] Logged: {temp}°C, {hum}%")
        except Exception as e:
            print(f"Error logging temperature: {e}")

        # Tunggu 1 jam (3600 detik)
        time.sleep(3600)


@app.route('/home')
def home():
    """Halaman Utama"""
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <html>
    <head>
        <title>Raspberry Pi Flask Server</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #eef2f7;
                text-align: center;
                margin-top: 50px;
            }}
            h1 {{ color: #0066cc; }}
            p {{ font-size: 18px; }}
        </style>
    </head>
    <body>
        <h1>Raspberry Pi Web Server (Flask)</h1>
        <p>
            Server berjalan dengan Flask!<br>
            Waktu sekarang: <b>{time_now}</b>
        </p>
        <p><a href="/temperature">Lihat Data Temperature</a></p>
    </body>
    </html>
    """


@app.route('/temperature')
def temperature():
    """Halaman Temperature dengan 12 jam terakhir"""
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ambil current reading
    try:
        current_temp = dht.temperature
        current_hum = dht.humidity
    except:
        current_temp = "Error"
        current_hum = "Error"

    # Ambil 12 data terakhir (offset 1 untuk skip yang paling baru)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT timestamp, temperature, humidity FROM temperature_log ORDER BY id DESC LIMIT 12 OFFSET 1')
    logs = c.fetchall()
    conn.close()

    # Buat tabel HTML untuk data
    table_rows = ""
    for log in logs:
        table_rows += f"""
        <tr>
            <td>{log[0]}</td>
            <td>{log[1]}°C</td>
            <td>{log[2]}%</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Raspberry Pi Temperature Server</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #eef2f7;
                text-align: center;
                margin-top: 30px;
            }}
            h1 {{ color: #0066cc; }}
            p {{ font-size: 18px; }}
            table {{
                margin: 20px auto;
                border-collapse: collapse;
                width: 600px;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #0066cc;
                color: white;
            }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Raspberry Pi Temperature Monitor</h1>
        <p>
            Waktu sekarang: <b>{time_now}</b><br>
            Current Reading: <b>{current_temp}°C</b> | Humidity: <b>{current_hum}%</b>
        </p>

        <h2>12 Jam Terakhir (Log Per Jam)</h2>
        <table>
            <tr>
                <th>Waktu</th>
                <th>Temperature</th>
                <th>Humidity</th>
            </tr>
            {table_rows if table_rows else "<tr><td colspan='3'>Belum ada data</td></tr>"}
        </table>

        <p><a href="/home">Kembali ke Home</a></p>
    </body>
    </html>
    """


if __name__ == '__main__':
    # Initialize database
    init_db()

    # Threading to save data every hour
    logger_thread = threading.Thread(target=log_data_hourly, daemon=True)
    logger_thread.start()

    print("Server running at http://0.0.0.0:8080")
    print("Saving data each hour to database")
    app.run(host='0.0.0.0', port=8080)