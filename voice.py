import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os
import re
import pyttsx3


recognizer = sr.Recognizer()
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def speak(text):
    clean_text = remove_emojis(text)
    engine = pyttsx3.init()
    engine.say(clean_text)
    engine.runAndWait()
    engine.stop()


def listen():
    fs = 44100
    duration = 5  # seconds

    print("🎤 Listening...")
    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='float32'
    )
    sd.wait()

    # Convert float32 → int16 (PCM)
    recording_int16 = np.int16(
        recording / np.max(np.abs(recording)) * 32767
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        write(f.name, fs, recording_int16)
        filename = f.name

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    os.remove(filename)

    try:
        text = recognizer.recognize_google(audio)
        print("You (voice):", text)
        return text.lower()
    except sr.UnknownValueError:
        return "sorry i did not understand"
    except sr.RequestError:
        return "speech service unavailable"
