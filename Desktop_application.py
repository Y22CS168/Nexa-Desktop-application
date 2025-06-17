import tkinter as tk
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import os
import threading
import requests

import requests

API_KEY = "ea422ddcafb2100743e10a69aa9e9bab"  # Replace with your full key
city = "Hyderabad"
BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={city}&units=metric"

response = requests.get(BASE_URL)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())

# === Voice Functions ===
def speechtx(x):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(x)
    engine.runAndWait()

def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            status_label.config(text="Recognizing...")
            data = recognizer.recognize_google(audio)
            print(f"You said: {data}")
            return data
        except sr.UnknownValueError:
            status_label.config(text="I didn't catch that.")
            speechtx("I didn't catch that. Please say it again.")
            return ""
        except sr.RequestError:
            status_label.config(text="API unavailable.")
            speechtx("Sorry, my speech service is unavailable.")
            return ""

def get_weather(city_name):
    try:
        complete_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units=metric"
        response = requests.get(complete_url)
        data = response.json()
        print("API response:", data)  # Debug line

        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temp = main["temp"]
            feels_like = main["feels_like"]
            result = f"The weather in {city_name} is {weather_desc} with a temperature of {temp}°C. It feels like {feels_like}°C."
            return result
        else:
            return "City not found."
    except Exception as e:
        print(f"Error: {e}")  # Print the actual error for debugging
        return "Unable to fetch weather right now."



def handle_commands():
    todo_list = []
    wake_command = sptext().lower()
    if "hello" in wake_command:
        speechtx("Hello! I'm Nexa. How can I help you?")
        while True:
            data1 = sptext().lower()

            if "your name" in data1:
                speechtx("My name is Nexa.")
            elif "created you" in data1:
                speechtx("I was created by Amisha.")
            elif "time now" in data1:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speechtx(f"The time is {current_time}")
            elif "youtube" in data1:
                webbrowser.open("https://www.youtube.com/")
            elif "google" in data1:
                webbrowser.open("https://www.google.com/")
            elif "github" in data1:
                webbrowser.open("https://www.github.com/")
            elif "linkedin" in data1:
                webbrowser.open("https://www.linkedin.com/in/shaik-amisha-32a190252/")
            elif "tell me a joke" in data1:
                joke = pyjokes.get_joke(language="en", category="neutral")
                print(joke)
                speechtx(joke)
            elif "music" in data1:
                add = "C:/Users/shaik/Music"
                listsong = os.listdir(add)
                if listsong:
                    print(listsong)
                    os.startfile(os.path.join(add, listsong[1]))
                else:
                    speechtx("No songs found in your music folder.")
            elif "ask a question" in data1:
                speechtx("I'd like to help. What is the question?")
                query = sptext().lower()
                url = f"https://www.google.com/search?q={query}"
                webbrowser.open(url)
                speechtx(f"Here are the search results for {query}")
            elif "task to my list" in data1:
                speechtx("What should I add to your to-do list?")
                task = sptext()
                todo_list.append(task)
                speechtx(f"I have added '{task}' to your to-do list.")
            elif "show my list" in data1:
                if todo_list:
                    speechtx("Here are your to-do items:")
                    for item in todo_list:
                        print(f"- {item}")
                        speechtx(item)
                else:
                    speechtx("Your to-do list is empty.")
            elif "delete my list" in data1:
                todo_list.clear()
                speechtx("I have cleared your to-do list.")
            elif "weather" in data1:
                speechtx("Which city's weather would you like to know?")
                city = sptext()
                weather_info = get_weather(city)
                speechtx(weather_info)
            elif "exit" in data1:
                speechtx("I hope you have enjoyed my service. Goodbye!")
                break

# === Start Listening in Thread ===
def start_nexa():
    threading.Thread(target=handle_commands).start()

# === GUI Setup ===
window = tk.Tk()
window.title("Nexa - Voice Assistant")
window.geometry("420x280")
window.resizable(False, False)

title_label = tk.Label(window, text="🎙️ Nexa - Your Voice Assistant", font=("Arial", 18, "bold"))
title_label.pack(pady=15)

status_label = tk.Label(window, text="Click the button and say 'hello' to start.", font=("Arial", 12))
status_label.pack(pady=10)

start_button = tk.Button(window, text="Start Nexa", font=("Arial", 14), bg="lightgreen", command=start_nexa)
start_button.pack(pady=30)

footer_label = tk.Label(window, text="Created by Amisha Shaik", font=("Arial", 10), fg="gray")
footer_label.pack(side="bottom", pady=10)

window.mainloop()
