from assistant.memory import remember, recall
from assistant.tasks import add_note, get_notes
from assistant.reminders import add_reminder
from assistant.ai_brain import ask_ai
from assistant.system_actions import (
    open_youtube,
    open_browser,
    open_vscode,
    open_notepad
)



def generate_response(intent, user_input):
    
    if intent == "store_name":
        name = user_input.split("my name is")[-1].strip()
        remember("username", name)
        return f"Nice to meet you, {name} 😊"

    elif intent == "get_name":
        name = recall("username")
        if name:
            return f"Your name is {name} 🙂"
        else:
            return "I don't know your name yet."
    
    elif intent == "add_note":
        note = user_input[4:].strip()  # removes "note"
        if not note:
            return "Please tell me what note to save."
        add_note(note)
        return "Note saved successfully 📝"

    elif intent == "show_notes":
        notes = get_notes()
        if not notes:
            return "You have no notes."
        return "Your notes:\n" + "\n".join(notes)

    elif intent == "exit":
        return "Goodbye! Have a great day 👋"
    
    elif intent == "add_reminder":
        try:
            parts = user_input.replace("remind me at", "").strip()
            time_part, message = parts.split("to", 1)

            time_str = time_part.strip().upper()
            message = message.strip()

            add_reminder(time_str, message)
            return f"Reminder set at {time_str} ⏰"

        except ValueError:
            return "Please use format: remind me at 7pm to do something"

    elif intent == "play_song":
        return open_youtube(user_input.replace("play song", "").strip())

    elif intent == "open_youtube":
        return open_youtube()

    # elif intent == "open_vscode":
    #     return open_vscode()

    elif intent == "open_browser":
        return open_browser()
    
    elif intent == "open_notepad":
        return open_notepad()

    elif intent == "open_vscode":
        return open_vscode()

    else:
        return ask_ai(user_input)
    
    
