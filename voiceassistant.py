import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
import requests
import threading

# ------------------- AI Logic --------------------

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the computer go to therapy? It had too many bytes of trauma.",
    "How does a computer get drunk? It takes screenshots.",
    "Why did the developer go broke? Because he used up all his cache.",
    "Why did the JavaScript developer leave? Because she didn't get arrays.",
    "Why do Java developers wear glasses? Because they can’t C#.",
    "404: Joke not found.",
    "What's a computer’s favorite beat? An algo-rhythm.",
    "Why was the developer always calm? Because he knew how to handle exceptions.",
    "Why don’t bachelors like Git? Because they are afraid to commit.",
    "Debugging: Being the detective in a crime movie where you are also the murderer.",
    "How many programmers does it take to change a light bulb? None, it's a hardware issue.",
    "There are only 10 types of people in the world: those who understand binary and those who don’t.",
    "Why do computers always sing? Because they have a byte!",
    "Why did Python break up with Java? Too much class.",
    "What did the router say to the doctor? It hurts when IP.",
    "Knock knock. Who's there? Recursion. Recursion who? Knock knock...",
    "Why are iPhones so sad? Because they don’t get a byte.",
    "The programmer got stuck in the shower because the instructions on the shampoo were: Lather, Rinse, Repeat.",
    "Why do programmers hate nature? It has too many bugs.",
    "Why was the AI assistant always tired? Too many sleepless algorithms."
]

def speak(text):
    app_output(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            app_output("🎙️ Listening...")
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice).lower()
            app_output(f"You said: {command}")
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
    speak(random.choice(jokes))

def get_weather():
    try:
        speak("Fetching weather...")
        response = requests.get("https://wttr.in/?format=3")
        if response.status_code == 200:
            speak(response.text)
        else:
            speak("Unable to fetch weather now.")
    except:
        speak("Could not reach the weather service.")

def get_news():
    try:
        speak("Getting today's top news headlines...")
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=your_api_key_here"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            for i, article in enumerate(articles[:5]):
                speak(f"Headline {i+1}: {article['title']}")
        else:
            speak("Could not fetch news.")
    except:
        speak("News service error.")

def introduce():
    speak("Hi, I'm your AI assistant. I can tell the time, open Google or YouTube, tell jokes, give weather reports, and more!")

def handle_command(command):
    if 'time' in command:
        tell_time()
    elif 'joke' in command:
        tell_joke()
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'weather' in command:
        get_weather()
    elif 'news' in command:
        get_news()
    elif 'who are you' in command or 'introduce yourself' in command:
        introduce()
    elif 'exit' in command or 'quit' in command or 'goodbye' in command:
        speak("Goodbye! Talk to you later.")
        return False
    else:
        speak("Sorry, I didn’t get that. Try asking something else.")
    return True

def run_assistant():
    speak("Hello! I'm ready to assist you.")
    running = True
    while running:
        command = listen()
        if command:
            running = handle_command(command)

# ------------------- GUI Setup --------------------

def app_output(text):
    output_text.config(state="normal")
    output_text.insert(tk.END, text + "\n")
    output_text.see(tk.END)
    output_text.config(state="disabled")

def start_voice_assistant():
    threading.Thread(target=run_assistant).start()

root = tk.Tk()
root.title("Voice Assistant AI")
root.geometry("700x500")
root.resizable(False, False)

title = tk.Label(root, text="🎤 Voice Assistant AI", font=("Arial", 20, "bold"))
title.pack(pady=10)

start_button = tk.Button(root, text="Start Listening", font=("Arial", 14), command=start_voice_assistant)
start_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20, font=("Courier", 10), state="disabled", wrap=tk.WORD)
output_text.pack(pady=10)

root.mainloop()