import cv2
import csv
import os
from datetime import datetime
import gpiozero
from pathlib import Path
from time import sleep

led = gpiozero.LED(pin=4)

EXPRESSIONS = {
    1: "senang",
    2: "sedih",
    3: "marah",
    4: "kaget",
    5: "nangis",
}

# Anchor paths to this module's directory
MODULE_DIR = Path(__file__).resolve().parent
base_output_dir = MODULE_DIR / "expressions"
metadata_file = base_output_dir / "captures_metadata.csv"

# Initialize webcam
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Webcam tidak terdeteksi!")
    exit()

# Reduce buffer size to minimize lag
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Initialize folders
for expr in EXPRESSIONS.values():
    (base_output_dir / expr).mkdir(parents=True, exist_ok=True)

if not metadata_file.exists():
    with metadata_file.open(mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "image_path"])


def flush_camera_buffer(cap, num_frames=5):
    """Flush old frames from camera buffer"""
    for _ in range(num_frames):
        cap.grab()


try:
    running = True
    while running:
        # Print the expressions menu
        print("\nKlik angka (1-4) untuk memilih ekpresi wajah, 0 untuk keluar.")
        for i, expr in enumerate(EXPRESSIONS.values()):
            print(f"{i + 1}. {expr}")

        # Listen to user's input until valid
        input_invalid = True
        choice: int = -1

        while input_invalid:
            try:
                choice = int(input("Masukkan angka: "))

                if choice == 0:
                    print("\nProgram dihentikan oleh pengguna.")
                    running = False
                    break

                if choice in EXPRESSIONS.keys():
                    input_invalid = False
                else:
                    print("Pilihan tidak valid. Masukkan angka 0-4.")
            except ValueError:
                print("Masukkan angka yang valid.")

        if not running:
            break

        # Flush buffer to get fresh frame
        flush_camera_buffer(cap)

        # Capture fresh frame
        ret, frame = cap.read()

        if not ret:
            print("Gagal mengambil gambar dari webcam.")
            continue

        # Save frame to corresponding folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = base_output_dir / EXPRESSIONS[choice] / f"{timestamp}_{EXPRESSIONS[choice]}.jpg"
        cv2.imwrite(str(image_path), frame)

        # Append metadata
        with metadata_file.open(mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, str(image_path)])

        print(f"✓ Ekspresi '{EXPRESSIONS[choice]}' disimpan: {image_path.name}")
        led.on()
        sleep(0.5)
        led.off()

except KeyboardInterrupt:
    print("\nProgram terhenti.")

finally:
    c