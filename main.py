import speech_recognition as sr
import webbrowser
import time
from time import ctime
import pyowm                # weather

import os                   # will help in removing audio files that we don't need anymore
import playsound
import random
from gtts import gTTS

r = sr.Recognizer()


def recordAudio(ask = False):
    with sr.Microphone() as source:
        if ask:
            playAudio(ask)
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            playAudio("Sorry, I didn't get that.")
        except sr.RequestError:
            playAudio("Something went wrong. Please try again later.")
        return voice_data


def playAudio(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) +'mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data): # maybe use dictionary
    if "what is your name" in voice_data:
        playAudio("My name is Moxy.")
    if "what time is it" in  voice_data:
        playAudio(ctime())
    if "weather" in voice_data:
        location = recordAudio("What location?")
        getWeather(location)
    if "search" in voice_data:
        search = recordAudio("What do you want to search?")
        getSearch(search)
    if "google maps" in voice_data:
        location = recordAudio("What is the location?")
        getLocation(location)
    if "stop" in voice_data:
        exit()

def getWeather(location):
    api_key = 'dca75cc32fc682fefba3d65c8971688f'
    open_weather_map = pyowm.OWM(api_key)
    mgr = open_weather_map.weather_manager()
    weather = mgr.weather_at_place(location).weather

    temp = weather.temperature("fahrenheit")
    curr_temp = round(temp["temp"])
    max_temp = round(temp["temp_max"])
    min_temp = round(temp["min_temp"])

    # need to add validation check for city
    # need to create weather look up for certain times
    
    playAudio("Current temperature in fahrenheit is " + str(curr_temp) + " with high " + str(max_temp) + " and low " + str(min_temp))


def getSearch(search):
    url = "https://google.com/search?q=" + search
    webbrowser.get().open(url)
    playAudio("Here is what I found for " + search)


def openYouTube():
    search = recordAudio("What would you like to watch on Youtube?")
    url = "https://www.youtube.com/results?search_query=" + search
    webbrowser.get().open(url)
    playAudio("Here is what I found on Youtube for " + search)


def getLocation(location):
    url = "https://google.nl/maps/place/" + location + "/&amp;"
    webbrowser.get().open(url)
    playAudio("Here is what I found for " + location)


time.sleep(1)
playAudio('How can I help you?')
while 1:
    voice_data = recordAudio()
    respond(voice_data)
