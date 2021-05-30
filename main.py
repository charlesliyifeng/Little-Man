import discord
#import pandas
from discord.ext import commands
from datetime import datetime
import os

TOKEN = os.environ['TOKEN']
curse_words = set()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
  print(f"logged in as {client.user}")

#list of commands
@client.command(name='hello', help='Say hello to the bot!')
async def say_hello(ctx):
  await ctx.send("Hello!")

@client.command(name='isJavascriptGood', help='Discover the correct opinion of Javascript.')
async def java_bad(ctx):
  await ctx.send("No")

#override on_message
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if check_time():
    reason = "chatting in class time"
    warning(message)
    await message.channel.send(f"You have been warned for {reason}")

  if check_swearing(message.content):
    reason = "profanity"
    warning(message)
    await message.channel.send(f"You have been warned for {reason}")
  
  #read commands
  await client.process_commands(message)


#message restriction in schooltime
def check_time():
  today = datetime.today()
  now = datetime.now()
  #12:30 - 13:15  13:00 - 13:35
  if today.weekday() < 5:
    if 8 < now.hour+now.minute/60 < 14.25:
      if today.weekday() == 2: #wednesday
        if 12 < now.hour+now.minute/60 < 12+7/12: #if in lunch time for wednesday:
          return False
      else:
        if 12.5 < now.hour+now.minute/60 < 12.25:
          return False
      return True
  return False

def load_curse_words():
  with open('./data/curse_words.txt') as file:
    for word in file:
      curse_words.add(word.strip('\n'))

def check_swearing(text):
  processed_text = text.lower()
  for word in curse_words:
    if word in processed_text:
      return True
  return False

def warning(message): #deletion of message and keeping trace of user
  pass

if __name__ == '__main__':
  load_curse_words()
  client.run(TOKEN)