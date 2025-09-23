from time import sleep

import gpiozero

# Setup LED on GPIO pin 14
led = gpiozero.LED(
    pin=14
)

# Hold the LED on for 1 second while the program runs
while True:
    led.on()
    sleep(1)
    led.off()