from time import sleep, time
import gpiozero

# Buttons setup
button_1 = gpiozero.Button(2)
button_2 = gpiozero.Button(3)

# LEDs setup
led_1 = gpiozero.LED(14)
led_2 = gpiozero.LED(15)

# Global scores
player1_score = 0
player2_score = 0

# Button actions
def button_1_action():
    global player1_score, player2_score
    print("[!] Button 1 pressed")
    player1_score += 1
    # player2_score -= 1
    led_1.on()
    sleep(0.1)
    led_1.off()

def button_2_action():
    global player1_score, player2_score
    print("[!] Button 2 pressed")
    player2_score += 1
    # player1_score -= 1
    led_2.on()
    sleep(0.1)
    led_2.off()

# Blink both LEDs for countdown
def blink_both_led():
    led_1.on()
    led_2.on()
    sleep(0.3)
    led_1.off()
    led_2.off()

def start_game(timer=10):
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0

    print("Game starting...")

    # Countdown before game
    for _ in range(3):
        blink_both_led()
        sleep(0.7)

    print("Go!")

    # Attach button callbacks
    button_1.when_pressed = button_1_action
    button_2.when_pressed = button_2_action

    # Run for 'timer' seconds
    start_time = time()
    while time() - start_time < timer:
        sleep(0.1)

    # Game over
    button_1.when_pressed = None
    button_2.when_pressed = None

    print("Game Over!")
    print(f"Player 1 score: {player1_score}")
    print(f"Player 2 score: {player2_score}")

    if player1_score > player2_score:
        print(">>> 🏆 Player 1 (GREEN) Wins! <<<")
        led_1.blink(0.2, 0.2, 5)
        led_1.on()
        sleep(5)
        led_1.off()
        print("[debug] led 1 should be on indefinitely")
    elif player2_score > player1_score:
        print(">>> 🏆 Player 2 (RED) Wins! <<<")
        led_2.blink(0.2, 0.2, 5)
        led_2.on()
        sleep(5)
        led_2.off()
        print("[debug] led 2 should be on indefinitely")
    else:
        print(">>> 🤝 It's a Draw! <<<")
        for _ in range(5):
            blink_both_led()
            sleep(0.2)

        led_1.on()
        led_2.on()
        sleep(5)

    print("[Game ended, run again for another game.]")

# Game duration
countdown = int(input("[?] Enter the game duration (seconds): "))
start_game(countdown)
