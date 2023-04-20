import pyttsx3

engine = pyttsx3.init()

def say(sentence):
    engine.say(f"{sentence}")
    engine.runAndWait()