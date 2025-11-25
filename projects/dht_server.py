import board
import adafruit_dht

from flask import Flask
import datetime

# Initialize Sensor
dht = adafruit_dht.DHT11(
    pin=board.D17,
    use_pulseio=False
)

app = Flask(__name__)

@app.route('/home')
def home():
    """Halaman Utama"""
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <html>
    <head>
        <title>
            Raspberry Pi Flask Server
        </title>
        <style>
            body {{
                font-family: Arial;
                back-ground-collor: #eef2f7;
                text-align: center;
                margin-top: 50px;
            }}
            h1 {{ color: #0066cc; }}
            p {{ font-size: 18px; }}
        </style>
    </head>
    <body>
        <h1>
            Raspberry Pi Web Server (Flask)
        </h1>
        <p>
            Server berjalan dengan Flask!
            Waktu sekarang: <b>{time}</b>
        </p>
    </body>
    </html>
    """

@app.route('/temperature')
def temperature():
    """Halaman Temperature"""
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = dht.temperature
    humidity = dht.humidity
    return f"""
    <html>
    <head>
        <title>
            Raspberry Pi Temperature Server
        </title>
        <style>
            body {{
                font-family: Arial;
                back-ground-collor: #eef2f7;
                text-align: center;
                margin-top: 50px;
            }}
            h1 {{ color: #0066cc; }}
            p {{ font-size: 18px; }}
        </style>
    </head>
    <body>
        <h1>
            Raspberry Pi Temperature Web Server (Flask)
        </h1>
        <p>
            Server berjalan dengan Flask!
            Menggunakan sensor DHT11
            
            Waktu sekarang: <b>{time}</b>
            Temperature: <b>{temperature}</b>
            Humidity: <b>{humidity}</b>
        </p>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("Flask server berjalan di http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080)