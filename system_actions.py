import webbrowser
import subprocess
import os
import sys

def open_youtube(search_query=None):
    if search_query:
        url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
    else:
        url = "https://www.youtube.com"
    webbrowser.open(url)
    return "Opening YouTube 🎵"

def open_browser():
    webbrowser.open("https://www.google.com")
    return "Opening browser 🌐"

# def open_vscode():
#     try:
#         subprocess.Popen(["code"])
#         return "Opening Visual Studio Code 💻"
#     except:
#         return "VS Code is not found on this system."
def open_vscode():
    possible_paths = [
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Users\home\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            subprocess.Popen([path])
            return "Opening Visual Studio Code 💻"

    return "VS Code not found on this system."

def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad 📝"
    except Exception as e:
        return f"Could not open Notepad: {e}"


def open_folder(path):
    if os.path.exists(path):
        os.startfile(path)
        return f"Opening folder {path}"
    return "Folder not found."
