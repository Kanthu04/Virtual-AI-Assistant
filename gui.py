import tkinter as tk
from tkinter import scrolledtext
import threading
import time

from assistant.nlp import detect_intent
from assistant.response import generate_response
from assistant.voice import speak, listen
from assistant.reminders import check_reminders


class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Personal AI Assistant")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.thinking_job = None

        self.create_widgets()
        self.start_reminder_thread()

    # ---------------- UI SETUP ---------------- #

    def create_widgets(self):
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#252526",
            fg="#d4d4d4",
            insertbackground="white"
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        self.user_input = tk.Entry(
            self.root,
            font=("Segoe UI", 11),
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        self.user_input.pack(padx=10, pady=5, fill=tk.X)
        self.user_input.bind("<Return>", self.send_text)

        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=10)

        self.send_button = tk.Button(
            button_frame,
            text="Send",
            width=12,
            bg="#007acc",
            fg="white",
            relief="flat",
            command=self.send_text
        )
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.voice_button = tk.Button(
            button_frame,
            text="🎤 Voice",
            width=12,
            bg="#007acc",
            fg="white",
            relief="flat",
            command=self.send_voice
        )
        self.voice_button.pack(side=tk.LEFT, padx=5)

    # ---------------- DISPLAY HELPERS ---------------- #

    def display_message(self, sender, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def type_message(self, sender, message, delay=25):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}: ")
        self.chat_area.config(state=tk.DISABLED)

        def write_char(i=0):
            if i < len(message):
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.insert(tk.END, message[i])
                self.chat_area.config(state=tk.DISABLED)
                self.chat_area.yview(tk.END)
                self.root.after(delay, write_char, i + 1)
            else:
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.insert(tk.END, "\n\n")
                self.chat_area.config(state=tk.DISABLED)

        write_char()

    # ---------------- THINKING ANIMATION ---------------- #

    def show_thinking(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "Assistant is thinking")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

        dots = ["", ".", "..", "..."]
        index = 0

        def animate():
            nonlocal index
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete("end-4c", tk.END)
            self.chat_area.insert(tk.END, dots[index % 4])
            self.chat_area.config(state=tk.DISABLED)
            self.chat_area.yview(tk.END)
            index += 1
            self.thinking_job = self.root.after(500, animate)

        animate()

    def stop_thinking(self):
        if self.thinking_job:
            self.root.after_cancel(self.thinking_job)
            self.thinking_job = None
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, "\n\n")
            self.chat_area.config(state=tk.DISABLED)

    # ---------------- TEXT MODE ---------------- #

    def send_text(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.user_input.delete(0, tk.END)
        self.display_message("You", user_text)

        threading.Thread(
            target=self.process_text_response,
            args=(user_text,),
            daemon=True
        ).start()

    def process_text_response(self, user_text):
        self.root.after(0, self.show_thinking)

        intent = detect_intent(user_text)
        response = generate_response(intent, user_text)

        self.root.after(0, self.stop_thinking)
        self.root.after(0, self.type_message, "Assistant", response)
        speak(response)

        if intent == "exit":
            self.root.after(1500, self.root.destroy)

    # ---------------- VOICE MODE ---------------- #

    def send_voice(self):
        threading.Thread(target=self.process_voice, daemon=True).start()

    def process_voice(self):
        self.display_message("Assistant", "🎤 Listening...")
        user_text = listen()

        self.display_message("You", user_text)
        self.show_thinking()

        intent = detect_intent(user_text)
        response = generate_response(intent, user_text)

        self.stop_thinking()
        self.type_message("Assistant", response)
        speak(response)

        if intent == "exit":
            time.sleep(1.5)
            self.root.destroy()

    # ---------------- REMINDERS ---------------- #

    def start_reminder_thread(self):
        threading.Thread(target=self.reminder_loop, daemon=True).start()

    def reminder_loop(self):
        while True:
            check_reminders()
            time.sleep(30)


if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()
