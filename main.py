import discord
import pandas as pd
import time
from discord.ext import commands
from datetime import datetime
import os
import multiprocessing

TOKEN = os.environ['TOKEN']
curse_words = set()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents,command_prefix='!')
users = []
admins = []
spam = {}
spam_detect = True
swear_detect = True
time_detect = True

@client.event
async def on_ready():
  print(f"logged in as {client.user}")

  global members
  #This will get all the members in the server
  for guild in client.guilds:
    for member in guild.members:
      if member == client.user:
        continue
      print(member)
      users.append(member)
      spam[str(member)] = 0
      if not (members['id'] == str(member)).any():
        row = {"id":member,"warnings":0}
        members = members.append(row,ignore_index=True)
        members.to_csv("./data/club_member.csv",index=False)
      
      #find admins
      for role in member.roles:
        if role.name == "admin" or role.name == "student leader/co leader":
          admins.append(str(member))
          print("admin")
          break

#list of commands
@client.command(name='hello', help='Say hello to the bot!')
async def say_hello(ctx):
  await ctx.send("Hello!")

@client.command(name='isJavascriptGood', help='Discover the correct opinion of Javascript.')
async def java_bad(ctx):
  await ctx.send("No")

@client.command(name='toggle_spam', help='turn on/off spam detection')
async def toggle_spam(ctx):
  global spam_detect
  spam_detect = not spam_detect
  if spam_detect:
    await ctx.send("Spam detection on")
  else:
    await ctx.send("Spam detection off")

@client.command(name='toggle_time', help='turn on/off time detection')
async def toggle_time(ctx):
  global time_detect
  time_detect = not time_detect
  if time_detect:
    await ctx.send("Time detection on")
  else:
    await ctx.send("Time detection off")

@client.command(name='toggle_swearing', help='turn on/off swearing detection')
async def toggle_swearing(ctx):
  global swear_detect
  swear_detect = not swear_detect
  if swear_detect:
    await ctx.send("Swear detection on")
  else:
    await ctx.send("Swear detection off")
  

#override on_message
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if str(message.author) not in admins:
    if spam_detect:
      spam[str(message.author)] += 1
      if spam[str(message.author)] > 6:
        await warning(message,"Spamming",True)
        return

    if time_detect and check_time():
      await warning(message,"chatting in class time")
      return

    if swear_detect and check_swearing(message.content):
      await warning(message,"profanity")
      return
  
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
        if 12.5 < hour+now.minute/60 < 13.25:
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

async def warning(message,reason,purge=False): #deletion of message and keeping trace of user
  author = str(message.author)
  await message.delete()
  await message.channel.send(f"{author} has been warned for {reason}")

  #delete all message by author
  if purge:
    await message.channel.purge(limit=10,check=lambda m:str(m.author)==author)

  #record warnings in df
  members.loc[members['id'] == author,"warnings"] += 1
  #update csv
  members.to_csv("./data/club_member.csv",index=False)
  #deliver punishment

def reset_spamming():
  while True:
    if spam_detect:
      for x in spam:
        spam[x] = 0
    time.sleep(3)

if __name__ == '__main__':
  #load csv
  members = pd.read_csv("./data/club_member.csv",index_col=False)
  #load curse words before running
  load_curse_words()
  x = multiprocessing.Process(target=reset_spamming,daemon=True)
  x.start()
  client.run(TOKEN)
  