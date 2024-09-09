import pyttsx3
import wikipedia
import os
import webbrowser
import speech_recognition as sr
import datetime
import pyaudio
import urllib.parse  # To handle URL encoding

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
user_name = "Sir"

def ask_name():
    global user_name
    speak("By the way, what should I call you?")
    user_name = take_command().capitalize()
    speak(f"Nice to meet you, {user_name}!")

def speak(audio):
    """Speaks out the provided text."""
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    """Greets the user according to the current time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning! Hope you're ready for a productive day!")
    elif 12 <= hour < 18:
        speak("Good afternoon! How can I assist you today?")
    else:
        speak("Good evening! How may I serve you tonight?")

def take_command():
    """Listens to and returns the user's voice command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
        except sr.RequestError:
            speak("Could not request results from Google. Please check your internet connection.")
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        return "none"

def open_application(app_name, path):
    """Opens an application if the path exists."""
    if os.path.exists(path):
        speak(f"Opening {app_name}.")
        os.startfile(path)
    else:
        speak(f"Sorry, I couldn't find {app_name} in the specified path.")

def search_youtube(video_name):
    """Searches for a video on YouTube based on the provided video name."""
    speak(f"Searching YouTube for {video_name}.")
    # Create a search query URL
    query = urllib.parse.quote(video_name)
    url = f"https://www.youtube.com/results?search_query={query}"
    # Open the URL in the browser
    webbrowser.open(url)
    speak("Here are the results from YouTube.")

def small_talk():
    speak("Would you like to hear a joke, a fun fact, or a motivational quote?")
    response = take_command().lower()
    if 'joke' in response:
        speak("Why don't skeletons fight each other? They don't have the guts!")
    elif 'fact' in response:
        speak("Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!")
    elif 'quote' in response:
        speak("Here's a quote for you: The only way to do great work is to love what you do, by Steve Jobs.")


def process_query(query):
    """Processes the user query and performs the corresponding action."""
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        try:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results for this topic. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, no relevant Wikipedia page found.")
        except Exception:
            speak("Sorry, I encountered an error while fetching information.")

    elif 'play' in query and 'on youtube' in query:
        video_name = query.replace("play", "").replace("on youtube", "").strip()
        search_youtube(video_name)

    elif 'open google' in query:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    
    elif 'open youtube' in query:
        speak("Opening youtube.")
        webbrowser.open("https://www.youtube.com/")

    elif 'open stackoverflow' in query:
        speak("Opening StackOverflow.")
        webbrowser.open("https://stackoverflow.com")

    elif 'the time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {str_time}")

    elif 'open code' in query:
        open_application("Visual Studio Code", "C:\\Users\\Karan Chavda\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

    elif 'open excel' in query:
        open_application("Microsoft Excel", "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")

    elif 'joke' in query or 'fact' in query or 'quote' in query:
        small_talk()

    elif 'open whatsapp' in query:
        # You need to update this with the actual path to WhatsApp.exe
        open_application("WhatsApp", "C:\\Users\\YourUsername\\AppData\\Local\\WhatsApp\\WhatsApp.exe")

    elif 'stop' in query or 'quit' in query:
        speak("Goodbye, sir! Have a nice day.")
        exit()

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        if query != "none":
            process_query(query)
