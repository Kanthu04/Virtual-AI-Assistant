import json
import os

MEMORY_FILE = "data/memory.json"

def load_memory():
    """Load memory from file"""
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as file:
        return json.load(file)

def save_memory(memory):
    """Save memory to file"""
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def remember(key, value):
    """Store a memory"""
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def recall(key):
    """Retrieve a memory"""
    memory = load_memory()
    return memory.get(key, None)
