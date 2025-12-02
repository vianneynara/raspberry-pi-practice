import board
import adafruit_dht
from flask import Flask, redirect
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
DB_NAME = 'temp_humi.db'


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


def get_last_timestamp():
    """Mengambil timestamp terakhir dari database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT timestamp FROM temperature_log ORDER BY id DESC LIMIT 1')
        result = c.fetchone()
        conn.close()

        if result:
            return datetime.datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        return None
    except Exception as e:
        print(f"Error getting last timestamp: {e}")
        return None


def log_data_periodically():
    """Stores the data (temperature and humidity) every hour this method being executed."""

    # Variables to calculate the initial wait time from latest timestamp
    last_time = get_last_timestamp()
    current_time = datetime.datetime.now()
    interval = 60  # 1 minute

    if last_time:
        # Calculate delta from the latest timestamp from DB
        time_diff = (current_time - last_time).total_seconds()

        if time_diff < interval:
            # still under the interval, wait until the end of the interval
            initial_wait = interval - time_diff
            print(f"Waiting {initial_wait:.1f} seconds to sync with last timestamp...")
        else:
            # if already more than the interval, start fresh
            seconds_into_minute = current_time.second
            initial_wait = interval - seconds_into_minute
            print(f"Last data was {time_diff:.1f}s ago. Starting fresh in {initial_wait:.1f}s...")

        time.sleep(initial_wait)

    # Main loop to log
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

        # Wait according to the interval
        time.sleep(interval)


@app.route('/')
def redirect_home():
    """Redirect to homepage"""
    return redirect('/home')

@app.route('/home')
def home():
    """Main page"""
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
            h1 {{ color: #8e26de; }}
            p {{ font-size: 18px; }}
        </style>
    </head>
    <body>
        <h1>Raspberry Pi Web Server (Flask)</h1>
        <p>
            Server berjalan dengan Flask!<br>
            Waktu sekarang: <b>{time_now}</b>
        </p>
        <div style="text-align:center; margin-top: 20px;">
            <button onclick="location.href='/current'">Lihat Data Temperatur dan Humidity</button>
        </div>
    </body>
    </html>
    """


@app.route('/current')
def current():
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
            h1 {{ color: #8e26de; }}
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
                background-color: #8e26de;
                color: white;
            }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Raspberry Pi Temperature Monitor</h1>
        <p>
            Waktu sekarang: <b>{time_now}</b><br>
            Temperature: <b>{current_temp}°C</b> | Humidity: <b>{current_hum}%</b>
        </p>

        <h2>12 Jam Terakhir (Log Per 1 Menit)</h2>
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
    logger_thread = threading.Thread(target=log_data_periodically, daemon=True)
    logger_thread.start()

    print("Server running at http://0.0.0.0:8080")
    print("Saving data periodically to database")
    app.run(host='0.0.0.0', port=8080)