import cv2
import csv
import os
import time
from datetime import datetime

# Interval pengambilan gambar (dalam detik)
INTERVAL = 5   # ubah sesuai kebutuhan, misal 1, 3, 10 detik, dll.

# Folder output
output_folder = "captured_images"
os.makedirs(output_folder, exist_ok=True)

# File CSV
csv_file = "webcam_data.csv"

# Inisiasi webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam tidak terdeteksi!")
    exit()

print(f"Program berjalan otomatis...")
print(f"Mengambil gambar setiap {INTERVAL} detik.")
print("Tekan CTRL + C untuk berhenti.")

# Jika CSV belum ada → buat header
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "image_path"])

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari webcam!")
            break

        # Waktu untuk metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"img_{timestamp}.jpg"
        filepath = os.path.join(output_folder, filename)

        # Simpan gambar
        cv2.imwrite(filepath, frame)
        print(f"Gambar disimpan: {filepath}")

        # Simpan metadata ke CSV
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, filepath])

        # Tunggu selama interval detik
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh pengguna.")

finally:
    cap.release()
    cv2.destroyAllWindows()
