import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import smtplib
import requests
import json

# Initialize speech recognition and synthesis engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            print(e)
            return None

# Function to send email
def send_email(receiver_email, subject, body):
    # Configure your email settings
    sender_email = 'sebopelophineous7@gmail.com'
    sender_password = '1234567'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(e)
        print("Failed to send email")

# Main function
def main():
    speak("Hello! I am Mr Phineous. How may  I help you today?")
    while True:
        query = recognize_speech()
        if query:
            # Convert query to lowercase for easier processing
            query = query.lower()

            # Perform actions based on user query
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif 'send email' in query:
                speak("Whom do you want to send the email?")
                receiver = recognize_speech()
                speak("What is the subject of the email?")
                subject = recognize_speech()
                speak("What should be the content of the email?")
                body = recognize_speech()
                send_email(receiver, subject, body)
            elif 'time' in query:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The current time is {current_time}")
            elif 'weather' in query:
                api_key = 'your_openweathermap_api_key'
                city = 'New York'  # You can ask for city name from the user
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
                response = requests.get(url)
                weather_data = response.json()
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                speak(f"The weather in {city} is {description} with a temperature of {temperature} degrees Celsius")
            elif 'exit' in query:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()
