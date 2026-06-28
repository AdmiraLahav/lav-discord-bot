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