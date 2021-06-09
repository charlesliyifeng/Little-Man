import discord
import pandas as pd
import time
from discord.ext import commands
from datetime import datetime
import os
import threading
import asyncio

TOKEN = os.environ['TOKEN']
curse_words = set()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix='!')
users = []
admins = []
helpers = []
spam = {}
help_requests = {"Quezard#5463": "testing"}
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
    await ctx.send("Hello! Good to see you.")


@client.command(name='isJavascriptGood',help='Discover the correct opinion of Javascript.')
async def java_bad(ctx):
    await ctx.send("No")


@client.command(name='load_members')
async def load_members(ctx=None):
    global members
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
            if not (members['id'] == member).any():
                row = {"id": member, "warnings": 0}
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
    if ctx:
        await ctx.send("members reloaded!")


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
        await ctx.send("Insufficent privilages")


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
        await ctx.send("Insufficent privilages")


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
        await ctx.send("Insufficent privilages")


@client.command(name='codingHelp', help='ask for help')
async def coding_help(ctx, *, message=None):
    message = message or "not specified"
    if ctx.author in help_requests:
        await ctx.message.delete()
        await ctx.send("request denied, you already have a pending help request.")
    else:
        help_requests[ctx.author.name] = message
        await ctx.message.delete()
        await ctx.send("request received, please await response from the helpers.")


@client.command(name='codingHelpResolve')
async def coding_help_resolve(ctx, name=None):
    if ctx.author in admins or ctx.author in helpers:
        if name in help_requests:
            del help_requests[name]
            await ctx.send("Request resolved!")
        else:
            await ctx.send("Request not found")
    else:
        await ctx.send("Only helpers and admins can resolve requests.")


#override on_message
@client.event
async def on_message(message):
    global spam
    if message.author == client.user:
        return

    if message.author not in admins:
        if spam_detect:
            print(spam[message.author])
            print(spam)
            spam[message.author] += 1
            if spam[message.author] > 6:
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


#message restriction in schooltime
def check_time():
    today = datetime.today()
    now = datetime.fromtimestamp(time.time() + 43200)
    hour = now.hour
    #12:30 - 13:15  13:00 - 13:35
    if today.weekday() < 5:
        if 8 < hour + now.minute / 60 < 14.25:
            if today.weekday() == 2:  #wednesday
                if 12 < hour + now.minute / 60 < 12 + 7 / 12:  #if in lunch time for wednesday:
                    return False
            else:
                if 12.5 < hour + now.minute / 60 < 13.25:
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


async def warning(message,
                  reason,
                  purge=False):  #deletion of message and keeping trace of user
    author = message.author
    await message.delete()
    await message.channel.send(f"{author} has been warned for {reason}")

    #delete all message by author
    if purge:
        await message.channel.purge(limit=10,
                                    check=lambda m: m.author == author)

    #record warnings in df
    members.loc[members['id'] == author, "warnings"] += 1
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


async def send_dm():
    global helpers
    while True:
        if bool(help_requests) and not check_time():
            for user in help_requests:
                message = f"{user} needs help with: {help_requests[user]}"
                print(message)
                for helper in helpers:
                    await helper.send(message)
        time.sleep(300)


def dm_wrapper():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(send_dm())
    loop.close()


if __name__ == '__main__':
    #load csv
    members = pd.read_csv("./data/club_member.csv", index_col=False)
    #load curse words before running
    load_curse_words()
    dm = threading.Thread(target=dm_wrapper, daemon=True)
    dm.start()
    client.run(TOKEN)
