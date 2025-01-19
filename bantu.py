import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import subprocess


chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Sir: {query}\nBun To: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant named Bun To."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response["choices"][0]["message"]["content"]
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        print(f"Error during chat completion: {e}")
        say("Sorry, I couldn't process your request.")
        return "Error in generating response."

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response["choices"][0]["message"]["content"]
        text += reply

        # Ensure the "Openai" directory exists
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        
        # Create a valid filename
        filename = prompt[:20].replace(" ", "_").replace("/", "_") + ".txt"
        with open(f"Openai/{filename}", "w") as f:
            f.write(text)
        say("Response saved successfully.")
    except Exception as e:
        print(f"Error during AI response: {e}")
        say("Sorry, I couldn't save the AI response.")

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=20)  # Adjust for long commands
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return "Listening timed out."
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return "I didn't catch that."
        except Exception as e:
            print(f"Error: {e}")
            return "Some error occurred. Sorry from Bun To."

def process_command(query):
    # Splitting the query by "and" to handle multiple commands
    commands = query.lower().split(" and ")
    
    for command in commands:
        command = command.strip()  # for Removing extra spaces

    

        # Predefined commands
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
            ["my website", "https://www.harshchaudhary.com.np"],
            ["linkedin","https://www.linkedin.com"],
            ["tiktok","https://www.tiktok.com"],
            ["instagram","https://www.instagram.com"]
        ]
        for site in sites:
            if f"open {site[0]}" in command:
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break
        
        # Open music
        if "open music" in command:
            open_music()

        # Close music
        elif "close music" in command:
            close_music()

        if "search for" in command:
            search_query = command.split("search for")[-1].strip()  # Get the search term
            if "on" in search_query:  # Handle 'search for ... on ...'
                parts = search_query.split("on")
                search_term = parts[0].strip()
                website = parts[1].strip()
                search_website(search_term, website)  # Call the function
            else:
                say("Please specify the website to search on.")
            continue
        
        elif "the time" in command:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            print(f"Sir, the time is {hour} hours and {minute} minutes.")
            say(f"Sir, The Time is {hour} and {minute} minutes right now!")

        # Open specific applications
        elif "open facetime" in command:
            os.system("open /System/Applications/FaceTime.app")
            print("Bantu: FaceTime Opened")
            say("Opening FaceTime.")

        elif "made" in command:
            print("Bantu: Sir, Techy Guy has made me.")
            say("Sir, Techy Guy has made me. He is a Nepali Programmer, YouTuber, and Content creator.")

        elif "what can you do" in command:
            print("Bantu : Sir, I can do everything that I have beene programmed to do.")
            say("Sir, I can do everything that I have been programmed to do.")

        elif "open my instagram" in command:
            print("Opening your instagram sir.")
            say("Opening your instagram sir.")
            webbrowser.open("https://www.instagram.com/theharshchaudhari/")

        elif "open pass" in command:
            os.system("open /Applications/Passky.app")
            print("Opening Passkey Sir")
            say("Opening Passky.")

        # Use AI for a specific prompt
        elif "using artificial intelligence" in command:
            ai(prompt=command)

        # Quit the assistant
        elif "stop your system" in command:
            print("Bantu: Thank you for having me, Have a great day Sir.")
            say("Thank you for having me, Have a great day !")
            exit()
        
        # Reset chat history
        elif "reset chat" in command:
            chatStr = ""
            say("Chat history reset.")
        
        # Default: Chat
        else:
            print("Chatting...")
            chat(command)

def open_music():
    musicPath = "/Users/harshchaudhary/Downloads/jhalle.mp3"
    if os.path.exists(musicPath):
        os.system(f"open {musicPath}")
        print("Bantu: Playing Your Music, Sir.")
        say("Playing your music.")
    else:
        print("Sir, I couldn't find the music file.")
        say("Music file not found.")

def close_music():
    try:
        # Terminate the default music player app
        os.system("pkill -f Music")  
        say("Music has been stopped.")
    except Exception as e:
        print(f"Error stopping music: {e}")
        say("Sorry, I couldn't stop the music.")



def take_and_process_commands():
    while True:
        query = takeCommand()
        if query.strip():
            process_command(query)

def search_website(query, site):
    # Define search URL templates for different websites
    search_urls = {
        "google": "https://www.google.com/search?q=",
        "youtube": "https://www.youtube.com/results?search_query=",
        "wikipedia": "https://en.wikipedia.org/wiki/",
        "amazon": "https://www.amazon.com/s?k="
    }
    
    # Check if the site is supported
    if site.lower() in search_urls:
        # Construct the search URL
        search_url = search_urls[site.lower()] + query.replace(" ", "+")
        # Open the search URL in a browser
        webbrowser.open(search_url)
        print(f"Searching for '{query}' on {site}.")
        say(f"Searching for {query} on {site}.")
    else:
        print(f"Sorry, I don't know how to search on {site}.")
        say(f"Sorry, I don't know how to search on {site}.")

if __name__ == '__main__':
    print('Welcome to Bun To A.I')
    say("Greetings Sir ! How can I assist you today ?")
    while True:
        query = takeCommand()
        if query.strip() == "":
            continue
        process_command(query)
