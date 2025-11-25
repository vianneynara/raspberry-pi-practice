import cv2
import csv
import os
from datetime import datetime

# Folder untuk menyimpan gambar
output_folder = "captured_images"
os.makedirs(output_folder, exist_ok=True)

# File CSV
csv_file = "webcam_data.csv"

# Inisiasi webcam (biasanya index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam tidak terdeteksi!")
    exit()

print("Tekan 'q' untuk berhenti mengambil gambar.")

# Jika file CSV belum ada → buat header
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "image_path"])

# Loop capture
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam!")
        break

    # Tampilkan gambar
    cv2.imshow("Webcam - Tekan 's' untuk simpan, 'q' untuk keluar", frame)

    key = cv2.waitKey(1)

    # tekan 's' untuk simpan gambar
    if key == ord('s'):
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

    # tekan 'q' untuk keluar
    if key == ord('q'):
        break

# Release
cap.release()
cv2.destroyAllWindows()
