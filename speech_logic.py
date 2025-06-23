# speech_logic.py
import speech_recognition as sr
import pyttsx3

def recognize_speech():
    """Listens to microphone and returns detected text & language code"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)  # automatic language detect
        return text
    except Exception as e:
        return f"Error: {e}"

def speak_text(text):
    """Read the given text aloud"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()