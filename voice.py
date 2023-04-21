import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def say(sentence):
    engine.say(f"{sentence}")
    engine.runAndWait()

say("Welcome to Vijay's aerodrome lookup service. How are you doing?")