from time import sleep

import gpiozero
from signal import pause
from gpiozero.tones import Tone

# Setup LED on GPIO pin 14
led = gpiozero.LED(
    pin=14
)
motion_sensor = gpiozero.MotionSensor(
    pin=15
)

# buzzer = gpiozero.Buzzer(pin=18)
buzzer = gpiozero.TonalBuzzer(pin=18)

button = gpiozero.Button(
    pin=3
)

alarm_is_on = False

print("Menunggu gerakan")

def motion_detected():
    global alarm_is_on
    alarm_is_on = True
    print("Motion detected!")
    while alarm_is_on:
        # buzzer.on()
        buzzer.play(Tone(200.0))
        led.on()
        sleep(0.1)
        # buzzer.off()
        buzzer.stop()
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