import discord
#import pandas
from datetime import datetime
import os

TOKEN = os.environ['TOKEN']
client = discord.Client()
curse_words = set()

@client.event
async def on_ready():
  print(f"logged in as {client.user}")

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if check_time():
    warning(message,"chatting in class time")

  if check_swearing(message.content):
    warning(message,"profanity")
  
  if message.content.startswith('!hello'):
    await message.channel.send("Hello!")
  elif message.content.startswith('!isJavascriptGood'):
    await message.channel.send("No")

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

def warning(message,reason): #deletion of message and keeping trace of user
  pass

if __name__ == '__main__':
  load_curse_words()
  client.run(TOKEN)