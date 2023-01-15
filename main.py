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
languagesResponses=[]

@client.event
async def on_ready():
    print(f"logged in as {client.user}")
    await load_members()
    spm = threading.Thread(target=reset_spamming, daemon=True)
    spm.start()

#list of commands
@client.command(name='hello', help='Say hello to the bot!')
async def say_hello(ctx):
    helloMessage=["Hello! Good to see you.","Hi!","Hello! I'm Litte Man."]
    await ctx.send(helloMessage[random.randint(0,2)])


@client.command(name='commands', help='list of commands')
async def commands(ctx):
  await ctx.send("Universal commands: !hello, !inspire, !isScriptGood [coding language] (Case sensitive) !codingHelp [message] (Case sensitive)")
  if ctx.author in admins:
    await ctx.send("Admin commands: !load_members, !toggle_spam, !toggle_time, !toggle_swearing, !toggle_helper, !resolve [name], !resolve_all")
  if ctx.author in helpers:
    await ctx.send("Helper commands: !toggle_helper, !resolve [name]")


@client.command(name='inspire',help='Get a random quote from a famouse person')#By DrKahl'sRobot
async def inspire(ctx):
    respond=requests.get("https://zenquotes.io/api/random")
    jsonData=json.loads(respond.text)
    await ctx.send(jsonData[0]['q']+' -'+jsonData[0]['a'])
@client.command(name='helloWorld', help='Hello World program in each languages')async def helloWorldFunction(ctx,arg=None):#NOT SURE IF IT WORKD OR NOT
	#By DrKahl'sRobot
	#By DrKahl'sRobot
    lang={
        'python':'print("Hello World!")',
        'javascript':'console.log("Hello world!")',
        'c':'''#include <stdio.h>

int main() {
   printf("Hello World!");
   return 0;
}''',
        'c#':'''using System;

namespace HelloWorld
{
    class Hello
    {         
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
    }
}''',
        'c++':'''#include <iostream>
using namespace std;

//Personal favourite

int main() {
    cout<<"Hello World!";
    return 0;
}''',
        'java':'''class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World!"); 
    }
}''',
        'ruby':'puts "Hello World!"',
        'perl':'''use strict;
use warnings;

print("Hello World!");''',
        'rust':'''fn main() {
    println!("Hello World!");
}'''
        }
    






    if arg.lower()in lang:
        await ctx.send(arg[0].upper()+arg[1:].lower()+':\n\n```'+lang[arg.lower()]+'```')
    else:
        await ctx.send("Sorry for unrecognized languages! Add more in main.py if you want.")#By DrKahl'sRobot

@client.command(name='isScriptGood',help='Discover the correct option for a specific coding language')#By DrKahl'sRobot
async def isScriptGood(ctx,arg=None):#27 languages
  lang = {
    'python':'Python is a high-level, interpreted, interactive and object-oriented scripting language. Python is designed to be highly readable. It uses English keywords frequently where as other languages use punctuation, and it has fewer syntactical constructions than other languages.',
    'javascript':'JavaScript (often shortened to JS) is a lightweight, interpreted, object-oriented language with first-class functions, and is best known as the scripting language for Web pages, but it\'s used in many non-browser environments as well.',
    'c':'C is a high-level and general-purpose programming language that is ideal for developing firmware or portable applications. Originally intended for writing system software, C was developed at Bell Labs by Dennis Ritchie for the Unix Operating System in the early 1970s.',
    'c#':'C# (pronounced "See Sharp") is a modern, object-oriented, and type-safe programming language. C# enables developers to build many types of secure and robust applications that run in . NET. C# has its roots in the C family of languages and will be immediately familiar to C, C++, Java, and JavaScript programmers.',
    'c++':'C++ (said C plus plus) is an object-oriented computer language created by notable computer scientist Bjorne Stroustrop as part of the evolution of the C family of languages. It was developed as a cross-platform improvement of C to provide developers with a higher degree of control over memory and system resources.',
    'java':'Java is an object-oriented programming language that produces software for multiple platforms. When a programmer writes a Java application, the compiled code (known as bytecode) runs on most operating systems (OS), including Windows, Linux and Mac OS.',
    'swift':'Swift is a general-purpose programming language built using a modern approach to safety, performance, and software design patterns. The goal of the Swift project is to create the best available language for uses ranging from systems programming, to mobile and desktop apps, scaling up to cloud services.',
    'r':'Although R is known as a programming language, many programmers refer to it as software that contains a language as well as a runtime environment. It includes conditionals, loops and user-defined recursive functions, as well as and input and output facilities that facilitate the use of predictive analytics.',
    'go':'Go (also called Golang or Go language) is an open source programming language used for general purpose. Go was developed by Google engineers to create dependable and efficient software. Most similarly modeled after C, Go is statically typed and explicit.',
    'html':'The HyperText Markup Language or HTML is the standard markup language for documents designed to be displayed in a web browser. It can be assisted by technologies such as Cascading Style Sheets (CSS) and scripting languages such as JavaScript.',
    'scala':'Scala is a strong statically typed general-purpose programming language which supports both object-oriented programming and functional programming. Designed to be concise, many of Scala\'s design decisions are aimed to address criticisms of Java. Scala.',
    'rust':'Rust is a multi-paradigm, general-purpose programming language designed for performance and safety, especially safe concurrency. It is syntactically similar to C++, but can guarantee memory safety by using a borrow checker to validate references.',
    'typescript':'TypeScript is a programming language developed and maintained by Microsoft. It is a strict syntactical superset of JavaScript and adds optional static typing to the language. It is designed for the development of large applications and transpiles to JavaScript. As it is a superset of JavaScript, existing JavaScript programs are also valid TypeScript programs.',
    'f#':'F# (pronounced F sharp) is a functional-first, general purpose, strongly typed, multi-paradigm programming language that encompasses functional, imperative, and object-oriented programming methods.',
    'perl':'Perl is a family of script programming languages that is similar in syntax to the C language. It is an older, open source, general use, interpreted language. Perl was developed with usability in mind. Its efficient design lets developers do a lot with a little bit of code.',
    'ruby':'Ruby is dynamically typed and uses garbage collection and just-in-time compilation. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming. According to the creator, Ruby was influenced by Perl, Smalltalk, Eiffel, Ada, BASIC, and Lisp.',
    'kotlin':'Kotlin is a cross-platform, statically typed, general-purpose programming language with type inference. Kotlin is designed to interoperate fully with Java, and the JVM version of Kotlin\'s standard library depends on the Java Class Library, but type inference allows its syntax to be more concise. Kotlin mainly targets the JVM, but also compiles to JavaScript (e.g., for frontend web applications using React) or native code via LLVM (e.g., for native iOS apps sharing business logic with Android apps). Language development costs are borne by JetBrains, while the Kotlin Foundation protects the Kotlin trademark.',
    'basic':'BASIC (Beginners\' All-purpose Symbolic Instruction Code) is a family of general-purpose, high-level programming languages designed for ease of use. The original version was created by John G. Kemeny, Thomas E. Kurtz and Mary Kenneth Keller at Dartmouth College in 1964. They wanted to enable students in non-scientific fields to use computers. At the time, nearly all computers required writing custom software, which only scientists and mathematicians tended to learn.',
    'sql':'Basically, SQL stands for Structured Query Language which is basically a language used by databases. This language allows to handle the information using tables and shows a language to query these tables and other objects related (views, functions, procedures, etc.).',
    'php':'PHP is a server side scripting language that is embedded in HTML. It is used to manage dynamic content, databases, session tracking, even build entire e-commerce sites. It is integrated with a number of popular databases, including MySQL, PostgreSQL, Oracle, Sybase, Informix, and Microsoft SQL Server.',
    'dart':'Dart is an object-oriented, class-based, garbage-collected language with C-style syntax. It can compile to either native code or JavaScript, and supports interfaces, mixins, abstract classes, reified generics and type inference.',
    'elixir':'Elixir is a functional, concurrent, general-purpose programming language that runs on the BEAM virtual machine which is also used to implement the Erlang programming language. Elixir builds on top of Erlang and shares the same abstractions for building distributed, fault-tolerant applications.',
    'clojure':'Clojure is a dialect of Lisp, and shares with Lisp the code-as-data philosophy and a powerful macro system. Clojure is predominantly a functional programming language, and features a rich set of immutable, persistent data structures.',
    'julia':'Julia is a high-level, high-performance, dynamic programming language. While it is a general-purpose language and can be used to write any application, many of its features are well suited for numerical analysis and computational science. Tier 3: 32-bit ARM, PowerPC, AMD (ROCm) GPUs.',
    'pascal':'Pascal is an imperative and procedural programming language, designed by Niklaus Wirth as a small, efficient language intended to encourage good programming practices using structured programming and data structuring. It is named in honour of the French mathematician, philosopher and physicist Blaise Pascal.',
    'matlab':'MATLAB is an abbreviation for "matrix laboratory." While other programming languages usually work with numbers one at a time, MATLAB® operates on whole matrices and arrays. Language fundamentals include basic operations, such as creating variables, array indexing, arithmetic, and data types.',
    'objective-c':'Objective-C is the primary programming language you use when writing software for OS X and iOS. It\'s a superset of the C programming language and provides object-oriented capabilities and a dynamic runtime.',
    'rank':'https://devathon.com/blog/wp-content/uploads/sites/2/2020/11/PYPL-graph.jpg \n https://devathon.com/blog/wp-content/uploads/sites/2/2020/11/TIOBE-graph.jpg \n https://devathon.com/blog/wp-content/uploads/sites/2/2020/11/GitHub-graph.jpg',
    'assembly':'In computer programming, assembly language (or assembler language), is any low-level programming language in which there is a very strong correspondence between the instructions in the language and the architecture\'s machine code instructions.',
    'shellscript':'A shell script is a computer program designed to be run by the Unix shell, a command-line interpreter. The various dialects of shell scripts are considered to be scripting languages. Typical operations performed by shell scripts include file manipulation, program execution, and printing text.',
    'lua':'Lua was originally designed in 1993 as a language for extending software applications to meet the increasing demand for customization at the time. It provided the basic facilities of most procedural programming languages, but more complicated or domain-specific features were not included; rather, it included mechanisms for extending the language, allowing programmers to implement such features. As Lua was intended to be a general embeddable extension language, the designers of Lua focused on improving its speed, portability, extensibility, and ease-of-use in development.',
    'bash':'Bash is a Unix shell and command language written by Brian Fox for the GNU Project as a free software replacement for the Bourne shell. First released in 1989, it has been used as the default login shell for most Linux distributions. Bash was one of the first programs Linus Torvalds ported to Linux, alongside GCC.',
    'coffeescript':'CoffeeScript is a programming language that compiles to JavaScript. It adds syntactic sugar inspired by Ruby, Python, and Haskell in an effort to enhance JavaScript\'s brevity and readability. Specific additional features include list comprehension and destructuring assignment.',
    'haskell':'Haskell is a general-purpose, statically-typed, purely functional programming language with type inference and lazy evaluation. Designed for teaching, research and industrial application, Haskell has pioneered a number of programming language features such as type classes, which enable type-safe operator overloading. Haskell\'s main implementation is the Glasgow Haskell Compiler (GHC). It is named after logician Haskell Curry.',
    'xml':'Extensible Markup Language (XML) is a markup language and file format for storing, transmitting, and reconstructing arbitrary data. It defines a set of rules for encoding documents in a format that is both human-readable and machine-readable. The World Wide Web Consortium\'s XML 1.0 Specification of 1998 and several other related specifications—all of them free open standards—define XML.'
  }

  if arg.lower() in lang:
    await ctx.send(lang[arg.lower()])
  else:
    await ctx.send("That is not a programming language (Type '!isScriptGood Rank' for help)")
  return

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
       

@client.command(name='codingHelp', help='ask for help')
async def coding_help(ctx, *, message=None):
  message = message or "not specified"
  if ctx.author.name in help_requests:
    await ctx.message.delete()
    await ctx.send("request denied, you already have a pending help request.")
  else:
    if len(message)<2:
                        await ctx.send('Oof, please send a request for')
                        return
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
