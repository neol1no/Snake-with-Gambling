import json
import os

SAVE_FILE = "save_data.json"

def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    else:
        return {"total_eggs": 0}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def reset_save():
    default_data = {"total_eggs": 0}
    save_data(default_data)