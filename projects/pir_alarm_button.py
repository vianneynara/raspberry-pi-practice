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

button = gpiozero.Button(
    pin=3
)

alarm_is_on = False

print("Menunggu gerakan")

def motion_detected():
    global alarm_is_on
    print("Motion detected!")
    while alarm_is_on:
        led.on()
        sleep(0.1)
        led.off()
        sleep(0.1)

def button_pressed():
    global alarm_is_on
    print("Button pressed! Turning alarm off.")
    alarm_is_on = False


motion_sensor.when_motion = motion_detected
button.when_pressed = button_pressed

try:
    pause()
except KeyboardInterrupt:
    print("Menghentikan program")