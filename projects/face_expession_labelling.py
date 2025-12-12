import cv2
import csv
import os
from datetime import datetime
import gpiozero

led = gpiozero.LED(
    pin=4
)

EXPRESSIONS = {
    1: "senang",
    2: "sedih",
    3: "marah",
    4: "kaget",
}

base_output_dir = "expressions"
metadata_file = "metadata.csv"

# initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam tidak terdeteksi!")
    exit()

# initialize folders
for expr in EXPRESSIONS.values():
    os.makedirs(os.path.join(base_output_dir, expr), exist_ok=True)

if not os.path.exists(metadata_file):
    with open(metadata_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "image_path"])

try:
    while True:
        # print the expressions menu
        print("Klik angka (1-4) untuk memilih ekpresi wajah, 0 untuk keluar.")
        for i, expr in enumerate(EXPRESSIONS.values()):
            print(f"{i+1}. {expr}")

        # listen the user's input until valid
        input_invalid = True

        if input() == "0":
            print("\nProgram dihentikan oleh pengguna.")
            break

        choice: int = -1
        while input_invalid:
            choice: int = int(input("Pilih ekspresi: "))
            if choice in EXPRESSIONS.keys():
                input_invalid = False

        # capture the frame then save it to corresponding folder,
        # following choice folder under base_output_dir
        ret, frame = cap.read()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        cv2.imwrite(
            os.path.join(base_output_dir, EXPRESSIONS[choice], f"{timestamp} {EXPRESSIONS[choice]}.jpg"),
            frame
        )
        # append metadata
        with open(metadata_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, os.path.join(base_output_dir, EXPRESSIONS[choice], f"{timestamp} {EXPRESSIONS[choice]}.jpg")])

        print(f"Ekspresi {EXPRESSIONS[choice]} disimpan.")
        led.on()


except KeyboardInterrupt:
    print("\nProgram terhenti.")

finally:
    cap.release()
    cv2.destroyAllWindows()