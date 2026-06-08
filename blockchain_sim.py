import json
import os

DATA_PATH = "data/medicines.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def add_medicine(med_id, name, batch, expiry, manufacturer):
    data = load_data()
    data[med_id] = {
        "name": name,
        "batch": batch,
        "expiry": expiry,
        "manufacturer": manufacturer
    }
    save_data(data)

def verify_medicine(med_id):
    data = load_data()
    return data.get(med_id, None)
