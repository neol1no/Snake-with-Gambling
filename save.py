import json
import os

SAVE_FILE_PATH = "save_data.json"  # Path to the save file

def load_data():
    """Load the saved data from the save file."""
    if os.path.exists(SAVE_FILE_PATH):
        with open(SAVE_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {"total_eggs": 0, "controls": "WASD"}  # Default data if no save file exists

def save_data(data):
    """Save the data to the save file."""
    with open(SAVE_FILE_PATH, 'w') as file:
        json.dump(data, file)

def reset_save():
    """Reset the save file to initial values."""
    default_data = {"total_eggs": 0, "controls": "WASD"}
    save_data(default_data)
