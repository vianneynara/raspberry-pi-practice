import cv2
import csv
import os
from datetime import datetime
import gpiozero
from pathlib import Path

led = gpiozero.LED(
    pin=4
)

EXPRESSIONS = {
    1: "senang",
    2: "sedih",
    3: "marah",
    4: "kaget",
}

# Step 1-2: Anchor paths to this module's directory
MODULE_DIR = Path(__file__).resolve().parent
base_output_dir = MODULE_DIR / "expressions"
metadata_file = MODULE_DIR / "metadata.csv"

# initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam tidak terdeteksi!")
    exit()

# initialize folders (Step 3: use pathlib and ensure dirs exist)
for expr in EXPRESSIONS.values():
    (base_output_dir / expr).mkdir(parents=True, exist_ok=True)

if not metadata_file.exists():
    with metadata_file.open(mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "image_path"])

try:
    running = True
    while running:
        # print the expressions menu
        print("Klik angka (1-4) untuk memilih ekpresi wajah, 0 untuk keluar.")
        for i, expr in enumerate(EXPRESSIONS.values()):
            print(f"{i+1}. {expr}")

        # listen the user's input until valid
        input_invalid = True

        choice: int = -1
        while input_invalid:
            choice = int(input("Masukkan angka:"))

            if choice == 0:
                print("\nProgram dihentikan oleh pengguna.")
                running = False
                break

            if choice in EXPRESSIONS.keys():
                input_invalid = False

        # capture the frame then save it to corresponding folder,
        # following choice folder under base_output_dir
        ret, frame = cap.read()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = base_output_dir / EXPRESSIONS[choice] / f"{timestamp} {EXPRESSIONS[choice]}.jpg"
        cv2.imwrite(str(image_path), frame)

        # append metadata
        with metadata_file.open(mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, str(image_path)])

        print(f"Ekspresi {EXPRESSIONS[choice]} disimpan.")
        led.on()


except KeyboardInterrupt:
    print("\nProgram terhenti.")

finally:
    cap.release()
    cv2.destroyAllWindows()