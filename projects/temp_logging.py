import csv
import time
import random
import os
import gpiozero

import board
import adafruit_dht

from datetime import datetime

LOGGING_FILE = "temp_log.csv"
INTERVAL = 3

dht = adafruit_dht.DHT11(
    pin=board.D17,
    use_pulseio=False
)

led = gpiozero.LED(
    pin=2
)

def read_sensors() -> tuple[float | None, float | None]:
    """Reads the temperature and humidity from the sensor.

    :return: temperature (float), humidity (float)
    """
    try:
        led.on()
        temperature = dht.temperature
        humidity = dht.humidity

        print(f'[INFO] Reading temperature, humidity: {temperature}, {humidity}')
        led.off()
        return temperature, humidity
    except RuntimeError as ex:
        print(f'[ERROR] {ex}')
        return None, None

def initialize_logging_file():
    try:
        with open(LOGGING_FILE, "x", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'temperature', 'humidity'])
        print("[INFO] Logging file initialized")
    except FileExistsError:
        print("[INFO] Logging file detected, using existing file")

def log(temperature, 
        humidity,
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ):
    with open(LOGGING_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, temperature, humidity])

def main():
    print("[INFO] Temperature and Humidity logging has been started")

    initialize_logging_file()

    try:
        while True:
            temp, humi = read_sensors()

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log(temp, humi)
            print(f"{timestamp}: Temperature at {temp}°C, with humidity of {humi}%")
            
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n\nData logging stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
