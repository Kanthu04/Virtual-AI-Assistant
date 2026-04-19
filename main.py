from assistant.nlp import detect_intent
from assistant.response import generate_response
from assistant.reminders import check_reminders
from assistant.voice import listen, speak
import threading
import time

def reminder_loop(): 
    while True:
        check_reminders()
        time.sleep(30)

def start_assistant():
    print("🤖 Virtual AI Assistant Started")
    print("Choose input mode:")
    print("T → Text")
    print("V → Voice")
    print("Type 'bye' or say 'bye' to exit\n")

    # Start reminder thread
    reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
    reminder_thread.start()

    while True:
        mode = input("Enter mode (T/V): ").strip().lower()

        if mode == "v":
            user_input = listen()
        else:
            user_input = input("You: ")

        intent = detect_intent(user_input)
        response = generate_response(intent, user_input)

        print("Assistant:", response)
        speak(response)
        time.sleep(0.3)

        if intent == "exit":
            break

if __name__ == "__main__":
    start_assistant()
