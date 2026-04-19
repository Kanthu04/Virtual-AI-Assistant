import json
from datetime import datetime
from assistant.voice import speak

REMINDER_FILE = "data/reminders.json"

def load_reminders():
    try:
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

# ✅ THIS FUNCTION WAS MISSING
def add_reminder(time_str, message):
    reminders = load_reminders()

    reminders.append({
        "time": time_str,
        "message": message,
        "triggered": False
    })

    save_reminders(reminders)

def normalize_time(time_str):
    time_str = time_str.strip().upper()

    # Remove dots from A.M. / P.M.
    time_str = time_str.replace(".", "")

    # Ensure space before AM/PM
    if time_str.endswith("AM") or time_str.endswith("PM"):
        if " " not in time_str:
            time_str = time_str[:-2] + " " + time_str[-2:]

    return time_str


def check_reminders():
    reminders = load_reminders()
    now = datetime.now()
    updated = False

    for reminder in reminders:
        if reminder["triggered"]:
            continue

        try:
            time_str = normalize_time(reminder["time"])

            reminder_time = datetime.strptime(
                time_str, "%I:%M %p"
            ).replace(
                year=now.year,
                month=now.month,
                day=now.day
            )

            if now >= reminder_time:
                alert = f"Reminder: {reminder['message']} ⏰"
                print("\nAssistant:", alert)
                speak(alert)

                reminder["triggered"] = True
                updated = True

        except ValueError:
            continue

    if updated:
        save_reminders(reminders)
