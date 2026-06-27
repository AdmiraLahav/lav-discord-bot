#+--------------+
#|My discord bot|
#+--------------+
#this bot is made for me to learn how to create bots like this and generally as a utility for my friends discord server
'''
THINGS TO REMMEMBER FOR ME
when creating a command the command name can be two things, the function name or *name="sendmsg"*

Explaining variable names:
ctx-the command itself when send in the server: ".say hello" is the ctx
*-lets the command access more than one word after the command name:
    without *: .say hello world -> hello
    with *: .say hello world -> hello world
also, * must come before the last parameter
msg/message-the input after the command name, could be named as anything along as it comes after "ctx,*,"

Simple Useable functions:
deleting the command message - ctx.message.delete()
getting author name - ctx.author
channel name - ctx.channel
server name - ctx.guild, if is equal to none was ran in DM's
using an @USERNAME - member: discord.Member
error handling - command_name.error(ctx, error)
'''
from math import inf

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
#import time
import asyncio
#from discord.ui import View, Button
#import re
#from collections import defaultdict

RESET = "\x1b[0m";
green_color = "\x1b[38;5;40m";
blue_color = "\x1b[38;5;12m";
red_color = "\x1b[38;5;196m";
yellow_color = "\x1b[38;5;226m";
program_name = f"[{blue_color}Custom Human Debug{RESET}]";
info = f"[{green_color}INF{RESET}]";
error = f"[{red_color}ERR{RESET}]";
warning = f"[{yellow_color}WRN{RESET}]";

# ---SETUP
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{info} {bot.user.name} is ready ")

@bot.event
async def on_member_join(member):
    await member.send("Welcome to the server")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    '''
    if "nigga" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} said 'nigga' and I deleted it")
    '''
    await bot.process_commands(message) # --- important

async def main():
    async with bot:
        await bot.load_extension("commands")
        await bot.start(token)

asyncio.run(main())