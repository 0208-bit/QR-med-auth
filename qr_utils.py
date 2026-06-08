def generate_qr(med_id, name, batch, expiry, manufacturer):
    import qrcode
    import os

    qr_data = f"ID:{med_id}, Name:{name}, Batch:{batch}, Exp:{expiry}, Mfg:{manufacturer}"
    print("QR DATA:", qr_data)  # ← This should show in terminal/console
    qr = qrcode.make(qr_data)

    os.makedirs("qr_codes", exist_ok=True)
    qr_path = f"qr_codes/{med_id}.png"
    qr.save(qr_path)

    return qr_path
