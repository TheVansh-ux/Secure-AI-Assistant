from gtts import gTTS
from playsound import playsound
import os
import datetime
import time
import speech_recognition as sr
import wikipedia
import webbrowser
import pywhatkit
import requests
import threading

def speak(text):
    #  Converts text to speech using Google's TTS engine, saves it as an MP3,
    # plays the sound, and then deletes the file.
    try:
        print(f"Assistant: {text}")

        tts= gTTS(text= text, lang= 'en', tld='co.uk', slow= False) #create the gTTS object

        audio_file= f"response_{int(time.time())}.mp3"
        tts.save(audio_file)
        playsound(audio_file)

        os.remove(audio_file)

    except Exception as e:
        print(f"Error in speech synthesis: {e}")
        print("Please check your internet connection.")

def listen():
    r= sr.Recognizer()
    r.pause_threshold = 1.5

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio= r.listen(source)

    try:
        print("Recognizing...")
        query= r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}\n")
        
        return query.lower()
    
    except sr.UnknownValueError:
        speak("I'm sorry, I could not understand that. Please try again.")
        return ""
    
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("I seem to be having trouble reaching my speech service.")
        return ""

def run_voice_assistant():
    speak("Hello, How can I help you?")
    while True:
        command= listen()

        if "wikipedia" in command:
            speak("Searching Wikipedia...")
            try:
                query= command.replace("wikipedia", "").strip()
                results= wikipedia.summary(query, sentences= 2)
                speak("According to Wikipedia")
                speak(results)

            except wikipedia.exceptions.PageError:
                speak(f"Sorry, I could not find any results for {query}.")
                      
            except wikipedia.exceptions.DisambiguationError:
                speak(f"{query} is ambiguous. Please be more specific.")

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "open chess" in command:
            speak("Opening Chess")
            webbrowser.open("https://www.chess.com")
        
        elif "play" in command:
            song= command.replace("play", "").strip()
            if song:
                speak(f"Playing {song} on YouTube.")
                pywhatkit.playonyt(song)
                break
            else:
                speak("What song would you like me to play?")
        

        elif "weather in" in command:
            city= command.split("in")[-1].strip()
            url= f'https://wttr.in/{city}?format=j1'
            try:
                response= requests.get(url)
                weather_data= response.json()

                if 'current_condition' in weather_data and weather_data['current_condition']:
                    current_condition = weather_data['current_condition'][0]
                    temp = current_condition['temp_C']
                    desc = current_condition['weatherDesc'][0]['value']
                    speak(f"The current weather in {city} is {temp} degrees Celsius with {desc}.")
                else:
                    speak(f"I'm sorry, I couldn't find weather data for {city}. Please try a larger nearby city.")
            
            except Exception as e:
                print(e)
                speak("I'm sorry, I couldn't retrieve the weather information right now.")  
            
        elif "shut down the computer" in command:
            speak("Are you sure you want to shut down the computer? Please say yes or no.")
            confirmation = listen()
            if 'yes' in confirmation:
                speak("Understood. Shutting down the computer in 3 seconds.")
                os.system("shutdown /s /t 3")
            else:
                speak("Shutdown cancelled.")
        
        elif "remind me to" in command:
            reminder_text= command.replace("remind me to", "").strip()
            speak("In how many minutes should I remind you?")
            time_command = listen()
            
            try:
                minutes= int(time_command)
                seconds= minutes*60
                def trigger_reminder():
                    speak(f"Reminder: It is time to {reminder_text}")
                timer= threading.Timer(seconds, trigger_reminder)
                timer.start()
                speak(f"Okay, I will remind you to {reminder_text} in {minutes} minutes.")

            except (ValueError, TypeError):
                speak("I'm sorry, I didn't understand the time. Please set the reminder again.")

        elif 'stop' in command or 'exit' in command or 'quit' in command or 'abort' in command:
            speak("Deactivating. Goodbye!")
            break

        time.sleep(1)


