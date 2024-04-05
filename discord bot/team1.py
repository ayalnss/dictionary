import discord
from discord.ext import commands, tasks
import requests
from PyDictionary import PyDictionary

# Initialize intents
intents = discord.Intents.default()

# Enable necessary intents
intents.messages = True  # Enable message-related events
intents.guilds = True  # Enable guild-related events
intents.members = True  # Enable member-related events

# Initialize our bot 
client = commands.Bot(command_prefix='!', intents=intents)

# Function to fetch a random word
def fetch_random_word():
    try:
        url = "https://random-word-api.herokuapp.com/word"
        response = requests.get(url)
        if response.status_code == 200:
            words = response.json()
            return words[0]  # Return the first word from the list
        else:
            print(f"Failed to fetch random word. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching random word: {e}")
        return None

def get_definitions(word):
    try:
        dictionary = PyDictionary()
        definitions = dictionary.meaning(word)
        return definitions
    except Exception as e:
        print(f"An error occurred while fetching definitions: {e}")
        return None

# Event that runs when the bot is ready
@client.event
async def on_ready():
    print("The bot is ready")
    print("------------------")

# Event to listen for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    word = message.content.strip().lower()

    definitions = get_definitions(word)

    if definitions:
        response = f"Definitions of '{word}':\n"
        for part_of_speech, meanings in definitions.items():
            response += f"{part_of_speech.capitalize()}:\n"
            response += "\n".join(meanings) + "\n"
        await message.channel.send(response)
    else:
        await message.channel.send(f"No definitions found for '{word}'")

    await client.process_commands(message)


@tasks.loop(hours=24)
async def word_of_the_day():
    word_of_the_day = fetch_random_word()
    if word_of_the_day:
        definition = get_definitions(word_of_the_day)
        if definition:
            channel_id = 1223047602329747476  
            channel = client.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(f"Word of the Day: {word_of_the_day}\nDefinition: {definition}")
                except Exception as e:
                    print(f"Failed to send word of the day message: {e}")
            else:
                print("Failed to find channel.")
        else:
            print(f"No definition found for '{word_of_the_day}'")
    else:
        print("Failed to fetch word of the day.")




client.run(' MTIyMDg3NzMzMjIyMzM2MTExNQ.GmjWn3.ny-ZtHPZy1HMy-3NIro5h5v2y2FTykMPx2rgRE')

