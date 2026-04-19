import json
import os

NOTES_FILE = "data/notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE, "r") as file:
        data = json.load(file)

        # Safety check (VERY IMPORTANT)
        if isinstance(data, list):
            return data
        else:
            return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)

def add_note(note):
    notes = load_notes()
    notes.append(note)
    save_notes(notes)

def get_notes():
    return load_notes()

