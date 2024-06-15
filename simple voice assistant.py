import tkinter as tk
from tkinter import filedialog
import subprocess
import speech_recognition as sr
import pyttsx3
import os
import time
import threading

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize variables
listening = False
listening_thread = None
task_history = []

def speak(text):
    engine.say(text)
    engine.runAndWait()

def log_task(task):
    task_history.append(task)
    task_display.insert(tk.END, task + "\n")
    task_display.see(tk.END)

def execute_command(command):
    try:
        if "open app" in command:
            if "calculator" in command:
                subprocess.Popen("calc.exe")
                log_task("Opened Calculator.")
            elif "calendar" in command:
                subprocess.Popen("start outlookcal:", shell=True)
                log_task("Opened Calendar.")
            elif "camera" in command:
                subprocess.Popen("start microsoft.windows.camera:", shell=True)
                log_task("Opened Camera.")
            elif "notepad" in command:
                subprocess.Popen("notepad.exe")
                log_task("Opened Notepad.")
            elif "file explorer" in command:
                subprocess.Popen("explorer.exe")
                log_task("Opened File Explorer.")
            elif "whatsapp" in command:
                subprocess.Popen("start whatsapp:", shell=True)
                log_task("Opened WhatsApp.")
            else:
                app_name = command.split("open app ")[1]
                open_system_app(app_name)

        elif "play video" in command:
            video_query = command.split("play video ", 1)[1]  # Get everything after "play video "
            os.system(f"start https://www.youtube.com/results?search_query={video_query}")
            log_task(f"Played YouTube video: {video_query}")
        elif "search" in command:
            search_query = command.split("search ", 1)[1]  # Get everything after "search "
            os.system(f"start https://www.google.com/search?q={search_query}")
            log_task(f"Google search for: {search_query}")
        else:
            # If no specific command is matched, attempt to open the app
            app_name = command.split("open ", 1)[1]  # Extract the app name
            open_system_app(app_name)

    except Exception as e:
        speak(f"Error executing command: {str(e)}")

def open_system_app(app_name):
    try:
        subprocess.Popen(f'start {app_name}', shell=True)
        log_task(f"Opened {app_name}.")
    except Exception as e:
        speak(f"Could not open {app_name}: {str(e)}")

def listen():
    global listening
    while listening:
        try:
            with sr.Microphone() as source:
                speak("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                command = recognizer.recognize_google(audio).lower()
                print(f"User said: {command}")
                speak(f"You said: {command}")
                log_task(f"You said: {command}")
                execute_command(command)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
        except sr.RequestError:
            speak("Oops! There was an issue with the speech recognition service.")
        except sr.WaitTimeoutError:
            continue
        time.sleep(5)  # Wait for 5 seconds before listening again

def start_listening():
    global listening, listening_thread
    if listening:
        listening = False
        if listening_thread is not None:
            listening_thread.join()
        update_listen_button()
    else:
        listening = True
        listening_thread = threading.Thread(target=listen)
        listening_thread.start()
        update_listen_button()

def update_listen_button():
    if listening:
        listen_button.config(text="Stop Listening", bg="red")
    else:
        listen_button.config(text="Start Listening", bg="green")

# Create a simple Tkinter GUI
root = tk.Tk()
root.title("Voice Assistant")

# Create frames for buttons and task display
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, padx=10, pady=10)

task_frame = tk.Frame(root)
task_frame.grid(row=1, column=0, padx=10, pady=10)

# Create and place buttons in a single row
listen_button = tk.Button(button_frame, text="Start Listening", command=start_listening, bg="green")
listen_button.grid(row=0, column=0, padx=5)

# Create a scrollable text widget to display tasks
task_display = tk.Text(task_frame, wrap=tk.WORD, height=10, width=50)
task_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

task_scrollbar = tk.Scrollbar(task_frame, command=task_display.yview)
task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_display.config(yscrollcommand=task_scrollbar.set)

# Run the main Tkinter loop
root.mainloop()
