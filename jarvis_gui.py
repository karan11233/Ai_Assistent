import tkinter as tk
import pyttsx3
import wikipedia
import os
import webbrowser
import speech_recognition as sr
import datetime
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishME():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        greeting = "Good morning!"
    elif hour >= 12 and hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    full_greeting = f"{greeting} I am Jarvis, sir. How may I assist you?"
    speak(full_greeting)
    return full_greeting

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except Exception as e:
        return "none"

def process_query():
    query = takeCommand()
    if 'stop' in query:
        speak("Stopping. Goodbye, sir!")
        return

    response = ""
    
    if 'wikipedia' in query:
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        response = f"According to Wikipedia: {results}"

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")
        response = "Opening YouTube."

    elif 'open google' in query:
        webbrowser.open("google.com")
        response = "Opening Google."

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Sir, the time is {strTime}"

    elif 'open code' in query:
        codePath = "C:\\Users\\Karan Chavda\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        if os.path.exists(codePath):
            os.startfile(codePath)
            response = "Opening Visual Studio Code."
        else:
            response = "Sorry, I couldn't find Visual Studio Code."

    elif 'open excel' in query:
        excelPath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
        if os.path.exists(excelPath):
            os.startfile(excelPath)
            response = "Opening Microsoft Excel."
        else:
            response = "Sorry, I couldn't find Excel."

    elif 'open whatsapp' in query:
        whatsappPath = "C:\\Users\\Karan Chavda\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
        if os.path.exists(whatsappPath):
            os.startfile(whatsappPath)
            response = "Opening WhatsApp."
        else:
            response = "WhatsApp not found."

    elif 'quit' in query or 'stop' in query:
        speak("Goodbye, sir! Have a nice day.")
        exit()
    
    if response:
        speak(response)

    return response

def run_voice_assistant():
    greeting = wishME()
    assistant_text.set(greeting)
    
    while True:
        response = process_query()
        if response:
            assistant_text.set(response)

def start_assistant():
    thread = threading.Thread(target=run_voice_assistant)
    thread.start()

# Create a GUI window
root = tk.Tk()
root.title("Voice Assistant - Jarvis")
root.geometry("500x400")

assistant_text = tk.StringVar()
assistant_label = tk.Label(root, textvariable=assistant_text, wraplength=400, justify='left', font=("Arial", 12))
assistant_label.pack(pady=20)

start_button = tk.Button(root, text="Start Assistant", command=start_assistant, width=20, font=("Arial", 12))
start_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, width=20, font=("Arial", 12))
exit_button.pack(pady=10)

root.mainloop()
