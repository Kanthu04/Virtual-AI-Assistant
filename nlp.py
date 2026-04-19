def detect_intent(text):
    text = text.lower().strip()

    # ---------------- EXIT ----------------
    if text in ["bye", "exit", "quit"]:
        return "exit"

    # ---------------- NAME MEMORY ----------------
    if "my name is" in text:
        return "store_name"

    if "what is my name" in text:
        return "get_name"

    # ---------------- NOTES ----------------
    # show notes MUST come before add note
    if "show notes" in text or "show my notes" in text:
        return "show_notes"

    if text.startswith("note"):
        return "add_note"

    # ---------------- REMINDERS ----------------
    if text.startswith("remind me"):
        return "add_reminder"

    # ---------------- SYSTEM ACTIONS ----------------
    if "play" in text and "song" in text:
        return "play_song"

    if "open youtube" in text:
        return "open_youtube"

    if "open" in text and ("vs" in text or "vscode" in text or "visual studio" in text):
        return "open_vscode"

    if "open" in text and "notepad" in text:
        return "open_notepad"

    if "open browser" in text:
        return "open_browser"

    # ---------------- DEFAULT CHAT ----------------
    return "chat"
