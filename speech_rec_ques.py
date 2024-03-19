# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 23:33:07 2023

@author: froot
"""

import speech_recognition as sr
import pyttsx3
import os

#initialize the recognizer
r = sr.Recognizer()

#Function to convert to 
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def get_unique_file_name(file_name):
    # Check if the original file name exists
    if not os.path.exists(file_name):
        return file_name

    # Split the file name into base name and extension
    base_name, extension = os.path.splitext(file_name)
    counter = 1

    while True:
        # Create a new file name with an incremented counter
        new_file_name = f"{base_name}_{counter}{extension}"

        # Check if the new file name exists
        if not os.path.exists(new_file_name):
            return new_file_name

        counter += 1

# Example usage
#file_name = "example.txt"
#unique_file_name = get_unique_file_name(file_name)
#print(unique_file_name)

with sr.Microphone() as source2:
    r.adjust_for_ambient_noise(source2, duration=0.2)
    
    audio2 = r.listen(source2)
    
    file_name = "ques_audio.wav"
    unique_file_name = get_unique_file_name(file_name)
    print(unique_file_name)
    
    with open(unique_file_name, 'wb') as f:
        f.write(audio2.get_wav_data())
    
    MyText = r.recognize_google(audio2)
    MyText = MyText.lower()
    
    print("Did you say "+MyText)
    SpeakText(MyText)