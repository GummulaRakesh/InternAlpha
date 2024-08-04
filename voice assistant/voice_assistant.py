import platform
import sys
import threading
import subprocess
import pyttsx3
import random
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import smtplib
import ctypes
import time
import requests
from ecapture import ecapture as ec
from PyQt5 import QtWidgets
from dotenv import load_dotenv
from mutagen.mp3 import MP3
import wolframalpha

# Load environment variables
load_dotenv()

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    """Speak the provided audio string."""
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    """Wish the user based on the current time of the day."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon Sir!")
    elif hour >= 17 and hour < 20:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir")
    speak("I am your Assistant. How can I help you?")

def take_command():
    """Listen for a command from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust to ambient noise
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return "None"
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Unable to recognize your voice.")
        return "None"
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return "None"
    return query.lower()

def send_email(to, content):
    """Send an email with the provided content."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        server.sendmail(os.getenv('EMAIL_USER'), to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        speak("I am not able to send this email")
        print(f"Error: {e}")

def get_song_duration(song_path):
    """Get the duration of the song in seconds."""
    if song_path.endswith('.mp3'):
        audio = MP3(song_path)
        return audio.info.length
    return 180  # Default duration if not an MP3 file

def play_song_with_default_player(song_path):
    """Play a song using the default music player."""
    if platform.system() == "Windows":
        os.startfile(song_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", song_path])
    else:  # Linux and other Unix-like systems
        subprocess.call(["xdg-open", song_path])

def play_all_songs(music_dir):
    """Play all songs from the specified music directory."""
    songs = [os.path.join(music_dir, song) for song in os.listdir(music_dir) if song.endswith('.mp3') or song.endswith('.wav')]
    if not songs:
        speak("No songs found in the directory.")
        return

    random.shuffle(songs)
    for song in songs:
        try:
            play_song_with_default_player(song)
            duration = get_song_duration(song)
            time.sleep(duration)
        except Exception as e:
            print(f"An error occurred while playing {song}: {e}")

def play_music_in_background(music_dir):
    """Play music in a separate thread."""
    music_thread = threading.Thread(target=play_all_songs, args=(music_dir,))
    music_thread.start()

def handle_query(query, output_widget):
    """Handle the user's query and execute the corresponding action."""
    if 'wikipedia' in query:
        search_wikipedia(query, output_widget)
    elif 'open youtube' in query:
        open_website("youtube.com", "Opening YouTube")
    elif 'open google' in query:
        open_website("google.com", "Opening Google")
    elif 'open stack overflow' in query:
        open_website("stackoverflow.com", "Opening Stack Overflow")
    elif 'play music' in query:
        speak("Playing music")
        music_dir = "C:\\Users\\admin\\Desktop\\songs"  # Adjust this path as needed
        try:
            play_music_in_background(music_dir)
        except FileNotFoundError:
            speak("Music directory not found.")
        except Exception as e:
            speak(f"An error occurred: {e}")
    elif 'the time' in query:
        tell_time(output_widget)
    elif 'email to' in query:
        send_email_to(query, output_widget)
    elif 'how are you' in query:
        speak("I am fine, thank you. How are you, Sir?")
        output_widget.append("I am fine, thank you. How are you, Sir?")
    elif 'hello' in query:
        wish_me()
    elif 'fine' in query or 'good' in query:
        speak("It's good to know that you are fine")
        output_widget.append("It's good to know that you are fine")
    elif "what's your name" in query or "what is your name" in query:
        speak("My friends call me psycho")
        output_widget.append("My friends call me psycho")
    elif 'exit' in query:
        speak("Thanks for giving me your time")
        output_widget.append("Thanks for giving me your time")
        return False
    elif 'joke' in query:
        tell_joke(output_widget)
    elif 'search' in query or 'play' in query:
        search_web(query)
    elif 'lock window' in query:
        lock_window(output_widget)
    elif 'shutdown system' in query:
        shutdown_system(output_widget)
    elif 'empty recycle bin' in query:
        empty_recycle_bin(output_widget)
    elif "don't listen" in query or "stop listening" in query:
        stop_listening(output_widget)
    elif "where is" in query:
        locate_place(query, output_widget)
    elif "camera" in query or "take a photo" in query:
        take_photo(output_widget)
    elif "restart" in query:
        restart_system(output_widget)
    elif "hibernate" in query or "sleep" in query:
        hibernate_system(output_widget)
    elif "log off" in query or "sign out" in query:
        log_off_system(output_widget)
    elif "write a note" in query:
        write_note()
    elif "show note" in query:
        show_note()
    elif "weather" in query:
        get_weather(output_widget)
    elif 'calculate' in query:
        app_id = "XH6PKX-ET558QUERW"  # Replace with your actual WolframAlpha App ID
        client = wolframalpha.Client(app_id)
        indx = query.lower().split().index('calculate')
        query = query.split()[indx + 1:]
        res = client.query(' '.join(query))
        try:
            answer = next(res.results).text
            speak(f"The answer is {answer}")
            output_widget.append(f"The answer is {answer}")
        except StopIteration:
            speak("I'm sorry, I couldn't find the answer to your query.")
            output_widget.append("I'm sorry, I couldn't find the answer to your query.")
    return True

def search_wikipedia(query, output_widget):
    """Search Wikipedia for the given query."""
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=3)
    speak("According to Wikipedia")
    output_widget.append("According to Wikipedia:\n" + results)
    speak(results)

def open_website(url, message):
    """Open the specified website."""
    speak(message)
    webbrowser.open(url)

def tell_time(output_widget):
    """Tell the current time."""
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time is {str_time}")
    output_widget.append(f"The time is {str_time}")

def send_email_to(query, output_widget):
    """Send an email to the specified recipient."""
    try:
        speak("What should I say?")
        content = take_command()
        to = "rakeshraks976@gmail.com"  # Update with the actual recipient's email
        send_email(to, content)
        output_widget.append("Email has been sent!")
    except Exception as e:
        speak("I am not able to send this email")
        output_widget.append("Failed to send the email.")

def tell_joke(output_widget):
    """Tell a joke."""
    joke = pyjokes.get_joke()
    speak(joke)
    output_widget.append(joke)

def search_web(query):
    """Search the web for the given query."""
    query = query.replace("search", "").replace("play", "")
    webbrowser.open(query)

def lock_window(output_widget):
    """Lock the Windows system."""
    speak("Locking the device")
    ctypes.windll.user32.LockWorkStation()
    output_widget.append("Device locked")

def shutdown_system(output_widget):
    """Shut down the system."""
    speak("Shutting down the system")
    output_widget.append("System shutting down")
    subprocess.call('shutdown /p /f')

def empty_recycle_bin(output_widget):
    """Empty the recycle bin."""
    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
    speak("Recycle Bin emptied")
    output_widget.append("Recycle Bin emptied")

def stop_listening(output_widget):
    """Stop listening to commands for a specified duration."""
    speak("For how long do you want to stop listening to commands?")
    try:
        a = int(take_command())
        time.sleep(a)
        output_widget.append(f"Stopped listening for {a} seconds")
    except ValueError:
        speak("Invalid duration specified.")
        output_widget.append("Invalid duration specified.")

def locate_place(query, output_widget):
    """Locate the specified place on Google Maps."""
    query = query.replace("where is", "")
    location = query
    speak(f"User asked to locate {location}")
    webbrowser.open(f"https://www.google.nl/maps/place/{location}")
    output_widget.append(f"Located {location}")

def take_photo(output_widget):
    """Take a photo using the webcam."""
    ec.capture(0, "Jarvis Camera", "img.jpg")
    output_widget.append("Photo taken")

def restart_system(output_widget):
    """Restart the system."""
    subprocess.call(["shutdown", "/r"])
    output_widget.append("System restarting")

def hibernate_system(output_widget):
    """Hibernate the system."""
    speak("Hibernating")
    subprocess.call("shutdown /h")
    output_widget.append("System hibernating")

def log_off_system(output_widget):
    """Log off the system."""
    speak("Signing out")
    time.sleep(5)
    subprocess.call(["shutdown", "/l"])
    output_widget.append("Signing out")

def write_note():
    """Write a note to a file."""
    speak("What should I write?")
    note = take_command()
    with open('jarvis.txt', 'w') as file:
        speak("Should I include date and time?")
        snfm = take_command()
        if 'yes' in snfm or 'sure' in snfm:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            file.write(str_time)
            file.write(" :- ")
        file.write(note)
    speak("Note written")

def show_note():
    """Show the note from the file."""
    speak("Showing Notes")
    with open("jarvis.txt", "r") as file:
        notes = file.read()
        speak(notes)

def get_weather(output_widget):
    """Get the weather for a specified city."""
    api_key = os.getenv('WEATHER_API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("City name")
    city_name = take_command()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        y = data["main"]
        current_temperature = float(y["temp"]) - 273.15
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = data["weather"]
        weather_description = z[0]["description"]
        weather_report = (f" Temperature (in Celsius unit) = {current_temperature}"
                          f"\n atmospheric pressure (in hPa unit) = {current_pressure}"
                          f"\n humidity (in percentage) = {current_humidity}"
                          f"\n description = {weather_description}")
        speak(weather_report)
        output_widget.append(weather_report)
    else:
        speak("City Not Found")
        output_widget.append("City Not Found")

def voice_assistant(output_widget):
    """Start the voice assistant."""
    global running
    wish_me()
    listening = True

    while running:
        if listening:
            query = take_command()
            if query == "None":
                continue
            listening = handle_query(query, output_widget)

    speak("Assistant has been stopped.")
    output_widget.append("Assistant has been stopped.")

class VoiceAssistantApp(QtWidgets.QMainWindow):
    """Main application window for the voice assistant."""
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the UI components."""
        self.setWindowTitle("Voice Assistant")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.output_widget = QtWidgets.QTextEdit(self)
        self.output_widget.setReadOnly(True)
        self.layout.addWidget(self.output_widget)

        self.start_button = QtWidgets.QPushButton("Start Assistant", self)
        self.start_button.clicked.connect(self.start_assistant)
        self.layout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton("Stop Assistant", self)
        self.stop_button.clicked.connect(self.stop_assistant)
        self.layout.addWidget(self.stop_button)

        self.assistant_thread = None

    def start_assistant(self):
        """Start the voice assistant."""
        global running
        if self.assistant_thread is None or not self.assistant_thread.is_alive():
            running = True
            self.assistant_thread = threading.Thread(target=voice_assistant, args=(self.output_widget,))
            self.assistant_thread.start()
            self.output_widget.append("Voice Assistant Started")

    def stop_assistant(self):
        """Stop the voice assistant."""
        global running
        if self.assistant_thread is not None and self.assistant_thread.is_alive():
            running = False
            self.assistant_thread.join(timeout=1)
            self.assistant_thread = None
            self.output_widget.append("Voice Assistant Going to Stop")

    def closeEvent(self, event):
        """Handle the window close event."""
        self.stop_assistant()
        event.accept()  # Accept the event to close the widget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = VoiceAssistantApp()
    mainWindow.show()
    sys.exit(app.exec_())
