from time import sleep

import gpiozero

# Setup LED on GPIO pin 14
led = gpiozero.LED(
    pin=14
)

# Hold the LED on for 5 seconds
led.on()
sleep(5)
led.off()