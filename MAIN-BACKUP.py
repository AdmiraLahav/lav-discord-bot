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
import time
import asyncio
from discord.ui import View, Button
import re
from collections import defaultdict

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

# role for secret commands
used_role="Stalin"

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

@bot.command(help="Show this message")
async def help(ctx):
    help_embed = discord.Embed(
        title="Bot Commands",
        description="Here are the commands this bot has:",
        color=discord.Color.blue()
    )

    for command in bot.commands:
        if command.hidden:
            continue

        command_name = f".{command.name}"
        command_description = command.help or "No description provided."

        help_embed.add_field(
            name=command_name,
            value=command_description,
            inline=False
        )

    await ctx.send(embed=help_embed)

@bot.command(help="Say hello to the sender")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

@bot.command(help="Answer to Stalin")
@commands.has_role(used_role)
async def Commie(ctx):
    await ctx.send("Yes comrade?")
@Commie.error
async def StalinError(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You are not a commie comrade!")

@bot.command(help="Dm a certain user")
@commands.has_role(used_role)
async def dm(ctx,member: discord.Member, *, msg):
    await member.send(msg)
    await ctx.author.send(f"sent to {member}: `{msg}`")
    await ctx.message.delete()
@dm.error
async def dmError(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("you do not have the permission to use this command")
#Make it reply to a replyed message: if I reply to someone with .reply word the bot will reply the word
@bot.command(help="Reply to the sender")
async def reply(ctx,*,msg):
    await ctx.reply("This is a relpy")

@bot.command(help="Create a custom poll")
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("❌")
    await poll_message.add_reaction("✅")

# -- WORD COUNTER:
def count_exact_word(message_text: str, searched_word: str) -> int:
    """
    Counts exact word matches.
    Example:
    word = "cat"
    "cat cat" = 2
    "catfish" = 0
    """
    word_pattern = r"\b" + re.escape(searched_word.lower()) + r"\b"
    matches = re.findall(word_pattern, message_text.lower())
    return len(matches)


@bot.command(name="wordlb", help="Count a certain word in specified channels")
async def word_leaderboard(
    ctx,
    searched_word: str,
    target_channels: commands.Greedy[discord.TextChannel]
):
    if ctx.guild is None:
        await ctx.send("This command only works inside a server.")
        return

    search_start_time = time.perf_counter()

    if target_channels:
        channels_to_search = target_channels
        searched_location = ", ".join(channel.mention for channel in channels_to_search)
        await ctx.send(f"Searching {searched_location} for: `{searched_word}`")
    else:
        channels_to_search = ctx.guild.text_channels
        searched_location = "the whole server"
        await ctx.send(f"Searching {searched_location} for: `{searched_word}`")

    await ctx.message.delete()

    user_word_counts = defaultdict(int)
    user_names = {}

    async with ctx.typing():
        for current_channel in channels_to_search:
            bot_permissions = current_channel.permissions_for(ctx.guild.me)

            if not bot_permissions.view_channel or not bot_permissions.read_message_history:
                continue

            try:
                async for message in current_channel.history(limit=None):
                    if message.author.bot:
                        continue

                    amount_found = count_exact_word(message.content, searched_word)

                    if amount_found > 0:
                        user_id = message.author.id
                        user_word_counts[user_id] += amount_found
                        user_names[user_id] = message.author.display_name

            except discord.Forbidden:
                continue
            except discord.HTTPException:
                continue

    elapsed_time = time.perf_counter() - search_start_time

    if not user_word_counts:
        await ctx.send(
            f"No one said `{searched_word}` in {searched_location}.\n"
            f"Elapsed time: `{elapsed_time:.2f}` seconds."
        )
        return

    sorted_users = sorted(
        user_word_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    leaderboard_lines = []

    top_amount = min(3, len(sorted_users))

    for index in range(top_amount):
        user_id, word_count = sorted_users[index]
        username = user_names.get(user_id, "Unknown user")
        leaderboard_lines.append(f"{index + 1}. {username} - {word_count}")

    command_user_id = ctx.author.id
    command_user_rank = None

    for index, user_data in enumerate(sorted_users, start=1):
        user_id, word_count = user_data

        if user_id == command_user_id:
            command_user_rank = index
            break

    top_user_ids = [user_id for user_id, count in sorted_users[:3]]

    if command_user_id not in top_user_ids:
        leaderboard_lines.append("-----")

        if command_user_rank is None:
            command_user_rank = len(sorted_users) + 1
            command_user_count = 0
        else:
            command_user_count = user_word_counts[command_user_id]

        leaderboard_lines.append(
            f"{command_user_rank}. {ctx.author.display_name} - {command_user_count}"
        )

    final_message = "\n".join(leaderboard_lines)

    await ctx.send(
        f"**Leaderboard for `{searched_word}`:**\n"
        f"```txt\n{final_message}\n```\n"
        f"Elapsed time: `{elapsed_time:.2f}` seconds."
    )

# fully personal command
@bot.command(help="spam a word a specified amount of times", hidden=True)
@commands.has_role(used_role)
async def spam(ctx,amount: int,*, msg):
    await ctx.message.delete()
    counter = 0;
    while counter < amount:
        await ctx.send(msg)
        counter+=1 

@bot.command(help="Find a specific message in given channel")
async def find(ctx,channel: discord.TextChannel,*,find_message):
    info_message=await ctx.send(f"Starting search for messages containing {find_message} in {channel}")

    messages = channel.history(oldest_first=False,limit=200)
    message_embed = discord.Embed(
        title=f"Found messages",
        description=f"Here are all the messages containing {find_message} in {channel}",
        color=discord.Color.blue()
        )
    # create an embed and find messages
    async for message in messages:
        if find_message in message.content:
            if message.author != bot.user:
                message_embed.add_field(
                    name=f"Message content: {message.content}\n",
                    value=f""+f"URL: {message.jump_url}",
                    inline=False
                )
    await ctx.send(embed=message_embed)
    await info_message.delete()

@bot.command(help="mention a certain user")
async def mention(ctx, *, member: discord.Member):
    await ctx.send(member)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)