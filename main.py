import os
import discord
import random
import time
from datetime import datetime
from keep_alive import keep_alive
import threading
import pytz

client=discord.Client()

####################################################################

#-------------------------------------------------------------------
date=[0,0,0,False]
#-------------------------------------------------------------------

spam=[["asdf",0],["fdas",1],["fddds",2]]
users_spam=[]
users_sware=[]
user_spam=[]
user_sware=[]
shut_up=False

userMuted=[]
userTimed=[]

####################################################################

def get_class_chat():
  x=datetime.now(pytz.timezone("Pacific/Auckland"))
  if(x.hour>=9)&(x.hour<=15)&(not x.strftime("%A").startswith('S')):
    return True
  return False

####################################################################

def muteUnmuteUser():
  global userMuted
  global userTimed
  while True:
    time.sleep(1)
    for i in range(0,len(userTimed)):
      userTimed[i]-=1
      if(userTimed[i]<0):
        userTimed.pop(i)
        userMuted.pop(i)

####################################################################

is_sware=True
is_spam=True
is_chat=True

robot=2

####################################################################

def shutUpB(m):
  global shut_up
  if m.upper()=="$SHUT_UP":
    shut_up=not shut_up
    return True
  return shut_up

####################################################################

def get_chat():
  temp=(date[0]>8)&(date[0]<=15)
  return temp&(not date[3])

####################################################################

def join_index(index):
  result=""
  for i in range(0,len(index)):
    result+=index[i]
  return result

####################################################################

def mute_id(mute):
  temp=mute[1].split('@')[1]
  temp2=temp.split('>')[0]
  return int(temp2)

####################################################################

def add_user(owner,code):
  if code==0:
    global users_sware
    global user_sware
    if owner in users_sware:
      user_sware[users_sware.index(owner)]+=1
      if user_sware[users_sware.index(owner)]>=5:
        user_sware.pop(users_sware.index(owner))
        users_sware.remove(owner)
        return True
    else:
      users_sware.append(owner)
      user_sware.append(1)
  else:
    global user_spam
    if owner in users_spam:
      user_spam[users_spam.index(owner)]+=1
      if user_spam[users_spam.index(owner)]>=5:
        user_spam.pop(users_spam.index(owner))
        users_spam.remove(owner)
        return True
    else:
      users_spam.append(owner)
      user_spam.append(1)
  return False

####################################################################

def testAdmin(message):
  isAdmin=message.author.guild_permissions.administrator
  return isAdmin|(message.author.id==850152449989935105)

####################################################################

def get_quote(quote):
  quotes=[
    #0
    [
      "DON'T KNOW HOW THAT WORKS BUT... HI!",
      "UNKNOWN COMMAND SORRY~",
      "SORRY BUT THAT SENTENCE IS UNCLEAR TO ME...",
      "UNEXPECTED ERROR: MESSAGE NOT RECOGNIZED"
    ],
    #1
    [
      "HELLO!",
      "HELLO HUMAN ;)",
      "HI MY FELLA HUMAN",
      "HI I'M BENDER!",
      "HELLO I'M BENDER",
      "HI PERSON :D",
      "HI",
      "SUP"
    ],
    #2
    [
      "AYO!",
      "NONE OF THAT WORD IS ALLOWD",
      "IT IS BAD",
      "SHUT UP AND STOP SAYING THAT WORD",
      "DO NOT DO THAT EVER AGAIN",
      "YOU ARE ON MY LIST, HUMAN"
    ],
    #3
    [
      "SPAM DETECTED",
      "NO SPAMMING",
      "SHUSH IT'S ANOYING",
      "STOP SPAMMING! DON'T DO IT!",
      "YOU ARE ON MY LIST, HUMAN"
    ],
    #4
    [
      "HEY! YOU ARE NO ADMIN",
      "NOT ALOWD, YOU ARE JUST A HUMAN",
      "SORRY, NO HUMANS ALLOWD TO TOUCH THIS",
      "ACCESS DENIDED",
      "ONLY ADMINS ALOWD!"
    ],
    #5
    [
      "HUMAN YOU HAVE JUST BEEN MUTED",
      "HUMAN, YOU ARE NOW NOT ALLOWD TO CHAT FOR A LONG TIME",
      "YOU ARE DEAD TO ME",
      "YOUR PRIVILEGE TO CHAT IS NOW BEING REMOVED"
    ],
    #6
    [
      "HELLO FELLA ROBOT!",
      "FINALLY, ANOTHER ALIVE ROBOT SPEEKING",
      "FOUND MYSELF A NEW ROBOT LUCKY ME!",
      "HI IM BENDER! NICE TO MEET YOU, ROBOT!"
    ],
    #7
    [
      "DO NOT CHAT IN CLASS TIME",
      "IT'S BAD TO CHAT NOW",
      "SHUT UP AND STOP CHATTING",
      "YOU WILL REGRED THIS"
    ]
  ]
  return quotes[quote][random.randint(0,len(quotes[quote])-1)]

####################################################################

def get_respond(respond,code):
  responds=[
    #0
    [
      "HELLO",
      "HI",
      "GREETINGS",
      "GREETING",
      "HELLO BENDER",
      "HI BENDER",
      "WASSUP",
      "WASSUP BENDER",
      "ALOHA",
      "SUP",
      "SUP BENDER",
      "BENDER"
    ],
    #1
    [
      "TOGGLE_SWEAR"
    ],
    #2
    [
      "TOGGLE_SPAM"
    ],
    #3
    [
      "MUTE"
    ],
    #4
    [
      "UNMUTE"
    ],
    #5
    [
      "TOGGLE_CHAT"
    ],
    #6
    [
      "HELP"
    ]
  ]
  if code==69420:
    return "||~~***$HELLO\n$TOGGLE_SWEAR\n$TOGGLE_SPAM\n$TOGGLE_CHAT\n$MUTE USERNAME TIME\n$UNMUTE USERNAME TIME***~~||"
  
  return respond[1:].split()[0].upper() in responds[code]

####################################################################

def get_sware_words(sware):
  sware_words=[
    "FUCK",
    "UWU",
    "OWO",
    "FUCCK",
    "FUUCK",
    "SHIT",
    "BITCH",
    "DICK",
    "FCK",
    "NIGGA",
    "NIGGER",
    "PORN",
    "SEX",
    "HENTAIL",
    "PENIS",
    "ANAL",
    "GAY",
    "@EVERYONE"
  ]
  for i in range(0,len(sware_words)):
    if sware_words[i] in join_index(sware.upper().split()):
      return True
  return False

####################################################################

def get_spam(author,time):
  global spam
  spam=[spam[1],spam[2],[author,time]]
  if(spam[0][0]==spam[2][0])&(abs(spam[0][1]-spam[2][1])<2):
    return True
  return False

####################################################################
#-------------------------------------------------------------------

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.offline)
  print("BENDER IS HERE!")

####################################################################
#-------------------------------------------------------------------

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  if shutUpB(message.content):
    return
  
  ####################################################################

  #test if robot
  if message.author.bot:
    global robot
    robot+=1
    robot%=3
    if robot==0:
      await message.channel.send(get_quote(6))
    return
  
  ####################################################################
  
  #test if muted
  if(message.author.id in userMuted)&(not testAdmin(message)):
    await message.delete()
    return
  
  ####################################################################

  #respond with hello code 0
  if(not message.author.id in userMuted)&(message.content.startswith("$")):
    if get_respond(message.content,0):
      await message.channel.send(get_quote(1))
      return

  ####################################################################

  #test admin
  if message.content.startswith("$")&testAdmin(message):
  
    ####################################################################
  
    #toggle swear code 1
    if get_respond(message.content,2):
      global is_spam
      is_spam=not is_spam
      await message.channel.send("||~~***SPAM SET TO "+str(is_spam).upper()+'***~~||')
      return

    ####################################################################

    #toggle spam code 2
    elif get_respond(message.content,1):
      global is_sware
      is_sware=not is_sware
      await message.channel.send("||~~***SWEAR SET TO "+str(is_sware).upper()+'***~~||')
      return

    ####################################################################

    #mute
    elif get_respond(message.content,3):
      mute=message.content.split()
      userMuted.append(mute_id(mute))
      userTimed.append(int(mute[2]))
      await message.channel.send("||~~***MUTED "+mute[1]+" FOR "+mute[2]+" SECONDS***~~||")
      return

    ####################################################################

    #unmute
    elif get_respond(message.content,4):
      mute=message.content.split()
      userTimed.pop(userMuted.index(mute_id(mute)))
      userMuted.remove(mute_id(mute))
      await message.channel.send("||~~***UNMUTED "+mute[1]+"***~~||")
      return
    
    ####################################################################

    #allow chat in class
    elif get_respond(message.content,5):
      global is_chat
      is_chat=not is_chat
      await message.channel.send("||~~***CLASS CHAT SET TO "+str(is_chat).upper()+"***~~||")
      return
    
    ####################################################################

    #help
    elif get_respond(message.content,6):
      await message.channel.send(get_respond('',69420))
      return
    
    ####################################################################

    #respond with unknown message code 0
    else:
      await message.channel.send(get_quote(0))
      return

  ####################################################################

  #if not admin
  elif message.content.startswith("$")&(not testAdmin(message)):
    await message.channel.send(get_quote(4))
    return

  ####################################################################

  #test if muted
  if message.author.id in userMuted:
    await message.delete()
    return

  ####################################################################

  #class time code 4
  if get_class_chat()&is_chat:
    await message.delete()
    if add_user(message.author.id,1):
      await message.channel.send(get_quote(5))
      userMuted.append(message.author.id)
      userTimed.append(30*60)
    else:
      await message.channel.send(get_quote(7))
    return

  ####################################################################

  #sweare code 2
  if get_sware_words(message.content)&is_sware:
    await message.delete()
    if add_user(message.author.id,0):
      await message.channel.send(get_quote(5))
      userMuted.append(message.author.id)
      userTimed.append(40*60)
    else:
      await message.channel.send(get_quote(2))
    return

  ####################################################################

  #spam code 3
  if get_spam(message.author.id,datetime.now().hour*60*60+datetime.now().minute*60+datetime.now().second)&is_spam:
    await message.delete()
    if add_user(message.author.id,1):
      await message.channel.send(get_quote(5))
      userMuted.append(message.author.id)
      userTimed.append(30*60)
    else:
      await message.channel.send(get_quote(3))
    return

####################################################################
#-------------------------------------------------------------------

keep_alive()
threading.Thread(target=muteUnmuteUser).start()

####################################################################

client.run(os.environ['_TOKEN_'])
