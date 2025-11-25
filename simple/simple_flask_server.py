from flask import Flask
import datetime

# Membuat instance Flask
app = Flask(__name__)

@app.route('/')
def home():
    """Halaman utama"""
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <html>
    <head>
        <title>Raspberry Pi Flask Server</title>
        <h1>Jording & Narring</h1>
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
        <h1>🌐 Raspberry Pi Web Server (Flask)</h1>
        <p>Server berjalan dengan Flask!</p>
        <p>Waktu sekarang: <b>{waktu}</b></p>
    </body>
    </html>
    """

# Jalankan server Flask
if __name__ == '__main__':
    print("✅ Flask server berjalan di http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080)
