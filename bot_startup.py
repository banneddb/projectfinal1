print("si")
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from bot_response import get_response
# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://example.com"
# Canvas API key
API_KEY = "p@$$w0rd"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Loading the token into the program
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot set-up below
intents: Intents = Intents.default()
intents.message_content = True #NOQA
client: Client = Client(intents=intents)

# Reading messages
async def send_message(message: Message, user_message:str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled)")
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Start-up for the Bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Entry Point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
