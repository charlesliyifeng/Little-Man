import discord
import pandas
from datetime import datetime
import os

TOKEN = os.environ['TOKEN']
client = discord.Client()

@client.event
async def on_ready():
  print(f"logged in as {client.user}")


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$hello'):
    await message.channel.send("Hello!")

def check_time(message):
  now = datetime.now()


def check_swearing():
  pass

client.run(TOKEN)