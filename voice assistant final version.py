from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask("Shilo's voice assistant" )
# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    
    engine.runAndWait()

def listen():
    """Capture audio input and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Network error.")
            return ""

def respond_to_command(command):
    """Process and respond to commands."""
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "hello" in command:
        speak("Hello! How can I assist you?")
    elif "home" in command:

        try:
            # Initialize geolocator
            geolocator = Nominatim(user_agent="voice_assistant")

            # Ask for the first location
            speak("Please specify the first location.")
            location_1_name = listen()
            location_1 = geolocator.geocode(location_1_name)

            # Ask for the second location
            speak("Please specify the second location.")
            location_2_name = listen()
            location_2 = geolocator.geocode(location_2_name)

            if location_1 and location_2:
                coords_1 = (location_1.latitude, location_1.longitude)
                coords_2 = (location_2.latitude, location_2.longitude)
                distance = geodesic(coords_1, coords_2).km
                speak(
                    f"The distance between {location_1_name} and {location_2_name} is approximately {distance:.2f} kilometers.")
            else:
                speak("I couldn't find one or both locations. Please try again.")
        except Exception as e:
            speak("An error occurred while processing the locations.")
            print(e)

    else:
        speak("I'm not sure how to help with that.")

# Main loop
if __name__ == "__main__":
    speak("Voice assistant is ready. Please say quit whenever you want to stop the program")
    while True:
        user_command = listen()
        if "exit" in user_command or "quit" in user_command:
            speak("Goodbye!")
            break
        respond_to_command(user_command)