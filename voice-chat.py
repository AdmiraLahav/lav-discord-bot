from math import inf

import discord
from discord.ext import commands
import logging
#from dotenv import load_dotenv
import os
import time
import asyncio
from discord.ui import View, Button
import re
from collections import defaultdict
from discord import FFmpegPCMAudio

@commands.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("Beginning In The End.mp3")

        print("Playing song")
        player = voice.play(source)

async def setup(bot):
    bot.add_command(join)