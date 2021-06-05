import discord
import pandas as pd
import time
from discord.ext import commands
from datetime import datetime
import os

TOKEN = os.environ['TOKEN']
curse_words = set()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents,command_prefix='!')
users = []
#spam={0,0,0}


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

@client.command(name='get_members', help='utility command: update list of members for the bot')
async def get_members(ctx):
  await ctx.message.delete()
  #This will get all the members in the server
  for guild in client.guilds:
    for member in guild.members:
      users.append(member)

#override on_message
@client.event
async def on_message(message):
  '''
    localTime=int(time.time())%3
  spam[2]+=1
  spam[1]+=1
  spam[0]+=1
  if spam[0]>=6:
    reason = "spam"
    warning(message)
    await message.channel.send(f"You have been warned for {reason}") 
  if localTime!=int(time.time())%3:
    localTime=int(time.time())%3
    spam[0]=spam[1]
    spam[1]=spam[2]
    spam[2]=0
  '''

  if message.author == client.user:
    return

  if check_time():
    await warning(message,"chatting in class time")

  if check_swearing(message.content):
    await warning(message,"profanity")
  
  #read commands
  await client.process_commands(message)


#message restriction in schooltime
def check_time():
  today = datetime.today()
  now = datetime.fromtimestamp(time.time()+43200)
  hour = now.hour
  #12:30 - 13:15  13:00 - 13:35
  if today.weekday() < 5:
    if 8 < hour+now.minute/60 < 14.25:
      if today.weekday() == 2: #wednesday
        if 12 < hour+now.minute/60 < 12+7/12: #if in lunch time for wednesday:
          return False
      else:
        if 12.5 < hour+now.minute/60 < 12.25:
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


async def warning(message,reason): #deletion of message and keeping trace of user
  await message.delete()
  await message.channel.send(f"{message.author} has been warned for {reason}")
  #record warnings in df
  members.loc[members['id'] == str(message.author),"warnings"] += 1
  #update csv
  members.to_csv("./data/club_member.csv",index=False)
  #deliver punishment

if __name__ == '__main__':
  #load csv
  members = pd.read_csv("./data/club_member.csv",index_col=False)
  #load curse words before running
  load_curse_words()
  client.run(TOKEN)
  