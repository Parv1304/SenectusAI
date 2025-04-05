import speech_recognition as sr
import pyttsx3

def speak(command):
    engine=pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def record():
    r=sr.Recognizer()
    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2,duration=0.2)
                print("Im listening")
                audio2=r.listen(source2)
                MyText=r.recognize_google(audio2)
                return MyText
        except:
            print("Error")
