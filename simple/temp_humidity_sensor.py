# requires adafruit's library

import time
import board
import adafruit_dht

dht = adafruit_dht.DHT11(
    pin=board.D17
)

def read_sensors() -> tuple[float | None, float | None]:
    """Reads the temperature and humidity from the sensor.

    :return: temperature (float), humidity (float)
    """
    try:
        temperature = dht.temperature
        humidity = dht.humidity

        print(f'[INFO] Reading temperature, humidity: {temperature}, {humidity}')
        return temperature, humidity
    except RuntimeError as ex:
        print(f'[ERROR] {ex}')
        return None, None

def main():
    print("Temperature and Humidity Sensor Test")

    try:
        while True:
            temperature, humidity = read_sensors()

            if temperature is not None and humidity is not None:
                if temperature > 30:
                    print(f'[OUT] High temperature detected: {temperature}')
                if humidity > 80:
                    print(f'[OUT] High humidity detected: {humidity}')

            time.sleep(3)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dht.exit()


if __name__ == '__main__':
    main()