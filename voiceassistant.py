# voice_assistant.py

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random

# Initialize the recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can try voices[1] for female voice

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"You said: {command}")
            return command
    except sr.WaitTimeoutError:
        speak("Sorry, I didn’t hear anything.")
        return ""
    except sr.UnknownValueError:
        speak("Sorry, I couldn’t understand that.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your connection.")
        return ""

def tell_time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The current time is {time}")

def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the computer go to therapy? It had too many bytes of trauma.",
        "How does a computer get drunk? It takes screenshots.",
    ]
    speak(random.choice(jokes))

def handle_command(command):
    if 'time' in command:
        tell_time()
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'joke' in command:
        tell_joke()
    elif 'exit' in command or 'quit' in command or 'goodbye' in command:
        speak("Goodbye! Have a great day!")
        return False
    else:
        speak("Sorry, I didn't understand that. Try asking something else.")
    return True

def main():
    speak("Hello! How can I help you today?")
    running = True
    while running:
        command = listen()
        if command:
            running = handle_command(command)

if __name__ == "__main__":
    main()