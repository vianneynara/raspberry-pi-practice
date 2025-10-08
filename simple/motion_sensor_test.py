from time import sleep

import gpiozero
from signal import pause

# Setup LED on GPIO pin 14
led = gpiozero.LED(
    pin=14
)
motion_sensor = gpiozero.MotionSensor(
    pin=15
)

print("Menunggu gerakan")

def motion_detected():
    print("Motion detected!")
    led.on()


def motion_ended():
    print("Motion ended!")
    led.off()


motion_sensor.when_motion = motion_detected
motion_sensor.when_no_motion = motion_ended

try:
    pause()
except KeyboardInterrupt:
    print("Menghentikan program")