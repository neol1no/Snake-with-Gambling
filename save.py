import json
import os

SAVE_FILE = "save_data.json"

def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    else:
        return {"total_eggs": 0, "egg_multiplier": 0, "growth_delay": 0, "eggs_per_level": 1}

def save_data(data):
    # Sicherstellen, dass die Datei überschrieben wird
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print(f"Save data written: {data}")  # Debug-Ausgabe für Überprüfung

def reset_save():
    # Standardwerte setzen
    default_data = {
        "total_eggs": 0,
        "egg_multiplier": 0,
        "growth_delay": 0,
        "eggs_per_level": 1
    }
    save_data(default_data)  # Standardwerte speichern
    print("Save file reset to default values.")  # Debug-Ausgabe

    # Erneutes Laden der gespeicherten Daten
    updated_data = load_save()
    print(f"Updated save data after reset: {updated_data}")  # Debug-Ausgabe

