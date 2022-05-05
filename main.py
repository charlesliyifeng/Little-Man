import discord
import pandas as pd
import time
from discord.ext import commands
from datetime import datetime
import os
import threading
from keep_alive import keep_alive
import pytz
import random
import json
import requests


TOKEN = os.environ['TOKEN']
curse_words = set()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix='!')
users = []
admins = []
lazy_helpers = []
helpers = []
spam = {}
help_requests = {}
spam_detect = True
swear_detect = True
time_detect = True


@client.event
async def on_ready():
    print(f"logged in as {client.user}")
    await load_members()
    spm = threading.Thread(target=reset_spamming, daemon=True)
    spm.start()

#list of commands
@client.command(name='hello', help='Say hello to the bot!')
async def say_hello(ctx):
    helloMessage=["Hello! Good to see you.","Hi!","Hello! I'm Litte Man"]
    await ctx.send(helloMessage[random.randint(0,2)])


@client.command(name='Inspire',help='Get a random quote from a famouse person')#By DrKahl'sRobot
async def inspire(ctx):
    respond=requests.get("https://zenquotes.io/api/random")
    jsonData=json.loads(respond.text)
    await ctx.send(jsonData[0]['q']+' -'+jsonData[0]['a'])
  

@client.command(name='commands', help='list of commands')
async def commands(ctx):
  await ctx.send("Universal commands: !hello, !Inspire, !isJavascriptGood, !isPythonGood, !CodingHelp [message] (Case sensitive)")
  if ctx.author in admins:
    await ctx.send("Admin commands: !load_members, !toggle_spam, !toggle_time, !toggle_swearing, !toggle_helper, !resolve [name], !resolve_all")
  if ctx.author in helpers:
    await ctx.send("Helper commands: !toggle_helper, !resolve [name]")


@client.command(name='isJavascriptGood',help='Discover the correct opinion of Javascript.')
async def javascript_good(ctx):
    await ctx.send("Absolutely!")


@client.command(name='isPythonGood',help='Discover the correct opinion of Python.')
async def python_good(ctx):
    await ctx.send("What's Python")


@client.command(name='load_members')
async def load_members(ctx=None):
    global members
    if ctx:
      if ctx.author not in admins:
        await ctx.send("Insufficient privileges")
        return
      else:
        await ctx.send("members reloaded!")
      
    helpers.clear()
    admins.clear()
    spam.clear()
    users.clear()
    #This will get all the members in the server
    for guild in client.guilds:
        for member in guild.members:
            if member == client.user:
                continue
            print(member)
            users.append(member)
            spam[member] = 0
            if not (members['id'] == int(member.id)).any():
                row = {"id": int(member.id), "warnings": 0}
                members = members.append(row, ignore_index=True)
                members.to_csv("./data/club_member.csv", index=False)

            #find admins
            for role in member.roles:
                if role.name == "admin" or role.name == "student leader/co leader":
                    admins.append(member)
                    print("admin")
                elif role.name == "helper":
                    helpers.append(member)
                    print("helper")


@client.command(name='toggle_spam', help='turn on/off spam detection')
async def toggle_spam(ctx):
    global spam_detect
    if ctx.author in admins:
        spam_detect = not spam_detect
        if spam_detect:
            await ctx.send("Spam detection on")
        else:
            await ctx.send("Spam detection off")
    else:
        await ctx.send("Insufficent privileges")


@client.command(name='toggle_time', help='turn on/off time detection')
async def toggle_time(ctx):
    global time_detect
    if ctx.author in admins:
        time_detect = not time_detect
        if time_detect:
            await ctx.send("Time detection on")
        else:
            await ctx.send("Time detection off")
    else:
        await ctx.send("Insufficent privileges")


@client.command(name='toggle_swearing', help='turn on/off swearing detection')
async def toggle_swearing(ctx):
    global swear_detect
    if ctx.author in admins:
        swear_detect = not swear_detect
        if swear_detect:
            await ctx.send("Swear detection on")
        else:
            await ctx.send("Swear detection off")
    else:
        await ctx.send("Insufficent privileges")
        
@client.command(name='toggle_helper', help='turn on/off helper role')
async def toggle_helper(ctx):
  if ctx.author in helpers or ctx.author in admins:
    if ctx.author in lazy_helpers:
      lazy_helpers.remove(ctx.author)
      await ctx.send("Welcome back!")
    else:
      lazy_helpers.append(ctx.author)
      await ctx.send(f"{ctx.author} is unavailable for helping at the moment.")
  else:
    await ctx.send("Insufficent privileges")
       

@client.command(name='CodingHelp', help='ask for help')
async def coding_help(ctx, *, message=None):
  message = message or "not specified"
  if ctx.author.name in help_requests:
    await ctx.message.delete()
    await ctx.send("request denied, you already have a pending help request.")
  else:
    help_requests[ctx.author.name] = message
    message = f"{ctx.author} needs help with: {help_requests[ctx.author.name]}"
    await ctx.message.delete()
    await ctx.send("request received, please await response from the helpers.")
    for helper in helpers:
      if helper not in lazy_helpers:
        await helper.send(message)
    
def find_name(message):
  for key in help_requests:
    if key in message:
      return True
  return False

@client.command(name='resolve', help='resolve the help request')
async def coding_help_resolve(ctx, name=None):
    if ctx.author in admins or (ctx.author in helpers and ctx.author not in lazy_helpers):
        if name in help_requests:
            del help_requests[name]
            try:
              await ctx.message.delete()
            except:
              pass
            await ctx.send("Request resolved!")
            for helper in helpers:
              async for message in helper.history(limit=100):
                if (not find_name(message.content)) and message.author == client.user:
                  await message.delete()
        else:
            try:
              await ctx.message.delete()
            except:
              pass
            await ctx.send("Request not found")
    else:
        await ctx.send("Only active helpers and admins can resolve requests.")

@client.command(name='resolve_all')
async def resolve_all(ctx):
  if ctx.author in admins:
    help_requests.clear()
    for helper in helpers:
      async for message in helper.history(limit=100):
        if message.author == client.user:
          await message.delete()
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("All requests resolved!")
  else:
    await ctx.send("Insufficent privileges")

#override on_message
@client.event
async def on_message(message):
    global spam
    if message.author == client.user:
        return

    if message.author not in admins:
        if spam_detect:
            if message.author in spam:
              spam[message.author] += 1
            else:
              spam[message.author] = 1
              
            if spam[message.author] > 2:
                await warning(message, "Spamming", True)
                return

        if time_detect and check_time():
            await warning(message, "chatting in class time")
            return

        if swear_detect and check_swearing(message.content):
            await warning(message, "profanity")
            return

    #read commands
    await client.process_commands(message)

@client.event
async def on_member_join(member):
  global members
  users.append(member)
  spam[member] = 0
  if not (members['id'] == int(member.id)).any():
    row = {"id": int(member.id), "warnings": 0}
    members = members.append(row, ignore_index=True)
    members.to_csv("./data/club_member.csv", index=False)


#message restriction in schooltime
def check_time():
    now = datetime.now()
    nz = pytz.timezone('Pacific/Auckland')
    now = now.astimezone(nz)
    hour = now.hour + now.minute / 60
    #12:30 - 13:15
    if now.weekday() < 5:
        if 9 <= hour < 15.25:
            if 12.5 <= hour < 13.25:
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
      if ' ' in word:
        if word in processed_text:
            with open('./data/swear_logs.txt','a') as file:
                file.write(processed_text+'\n')
            return True
      else:
        if word in processed_text.split():
            with open('./data/swear_logs.txt','a') as file:
                file.write(processed_text+'\n')
            return True
    return False


async def warning(message, reason, purge=False):  #deletion of message and keeping trace of user
    author = message.author
    await message.delete()
    await message.channel.send(f"{author} has been warned for {reason}")

    #delete all message by author
    if purge:
        await message.channel.purge(limit=10,check=lambda m: m.author == author)

    #record warnings in df
    members.loc[members['id'] == int(author.id), "warnings"] += 1
    #update csv
    members.to_csv("./data/club_member.csv", index=False)
    #deliver punishment


def reset_spamming():
  global spam
  while True:
    if spam_detect:
      for x in spam:
        spam[x] = 0
    time.sleep(3)


if __name__ == '__main__':
    #load csv
    members = pd.read_csv("./data/club_member.csv", index_col=False)
    #load curse words before running
    load_curse_words()
    keep_alive()
    client.run(TOKEN)
