import cv2
import os

med_id = input("Enter Medicine ID to decode QR: ").strip()
image_path = f"qr_codes/{med_id}.png"

# 1. Check file existence
if not os.path.exists(image_path):
    print(f"❌ File not found: {image_path}")
    exit()

# 2. Load image
img = cv2.imread(image_path)
if img is None:
    print("❌ Could not load image.")
    exit() 
else:
    print("✅ Image loaded.")

# 3. Decode QR
detector = cv2.QRCodeDetector()
data, bbox, _ = detector.detectAndDecode(img)

if bbox is not None and data:
    print("✅ QR code detected.")
    print("Data:", data)
else:
    print("❌ No QR code found or unreadable.")
