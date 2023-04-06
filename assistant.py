import speech_recognition as sr
import os
import pyttsx3
import openai

openai.api_key = "" #Use your OpenAI API key

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

# Initialize the speech recognition engine and microphone
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

# Initialize variables for the conversation and user/bot names
conversation = ""
user_name = "Vansh"
bot_name = "Jarvis"

# Start the conversation loop
while True:
    # Listen for user input using the microphone
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening")

    try:
        # Convert the user's speech to text using Google's speech recognition API
        user_input = r.recognize_google(audio)

        # Add the user's input to the conversation prompt
        prompt = user_name + ":" + user_input + "\n" + bot_name + ":"
        conversation += prompt

        # Generate a response to the user's input using OpenAI's text generation API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=conversation,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the response text from the OpenAI API response
        response_str = response["choices"][0]["text"].replace("\n", "")
        response_str = response_str.split(
            user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

        # Add the bot's response to the conversation and print it to the console
        conversation += response_str + "\n"
        print(response_str)

        # Speak the bot's response using the text-to-speech engine
        engine.say(response_str)
        engine.runAndWait()

    except sr.UnknownValueError:
        # Handle errors if the speech recognition API can't understand the user's speech
        print("Could not understand audio")
    except sr.RequestError as e:
        # Handle errors if there's a problem with the speech recognition API
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
