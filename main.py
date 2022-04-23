# Import libraries
import discord
from discord.ext import commands
import logging
import json
import re
#import youtube_dl
#from gtts import gTTS
#from io import BytesIO
import file_list

# Define bot, see discordpy website for logging to file instead of stdout
logging.basicConfig(level=logging.INFO)

#bot = discord.bot()

# Define behavior on bot login
#@bot.event
#async def on_ready():
#    print("Logged on as {0.user}!".format(bot))

# Define behavior on bot message receival
#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    print("Message from {0.author}: {0.content}".format(message))

#=================#
# Define commands #
#=================#
# I plan to only support once voice_client at a time
bot = commands.Bot(command_prefix="$")
#------#
# join #
#------#
@bot.command()
async def join(ctx):
    author = ctx.author
    # Author must have a voice connection to join
    if type(author) != discord.Member or author.voice == None:
        await ctx.send("You must be in a guild voice chat and use \join from a guild text chat.")
        return
    # If in a voice channel already, leave it
    if len(bot.voice_clients) != 0:
        await leave(ctx)

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("bark.mp3"))
    voice_client.play(source)

#-------#
# leave #
#-------#
@bot.command()
async def leave(ctx):
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm already not in a voice channel.")
        return

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("bark.mp3"))
    bot.voice_voice_clients[0].play(source, after=lambda e:
        await bot.voice_clients[0].disconnect())

#------#
# stop #
#------#
@bot.command()
async def stop(ctx):
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm not in a voice channel, I have nothing to stop doing.")
        return

    await bot.voice_clients[0].stop()

#------#
# play #
#------#
#@bot.command()
#async def play(ctx, url):
#    #match = re.search("\Ahttps://(www.youtube.com/watch?v=)|(youtu.be/)[a-zA-Z0-9]+", url)
#    #if match == None:
#        #await ctx.send("I don't understand the format of that link. Did you copy the full link?")
#
#    # Copied instructions from https://www.youtube.com/watch?v=MbhXIddT2YY
#    #server = ctx.message.server
#    #voice_client = bot.voice_client_in(server)
#    #player = await voice_client.create_ytdl_player(link)
#    #players[server.id] = player
#    #player.start()
#
#    # Get Youtube video, but don't predownload it (stream=True)
#    player = await YTDLSource.from_url(url, stream=True)
#    voice_client.play(player)

#------#
# tts  #
#------#
#@bot.command()
#async def tts(ctx, *, arg):
#    if voice_client == None:
#        await ctx.send("I'm not in a voice channel, I have nowhere to speak.")
#        return
#
#    mp3 = BytesIO()
#    tts = gTTS(text=arg, lang="en")
#    tts.write_to_fp(mp3)
#    voice_client.play(mp3)

#------#
# save #
#------#
@bot.command()
async def save(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("You didn't give me an attachment to save.")
        return

    for attachment in ctx.message.attachments:
        await ctx.send("Processing \"{}\"...".format(attachment.filename))
        await file_list.save_audio_file(ctx, attachment)
    await ctx.send("Done.")

#------#
# load #
#------#
@bot.command()
async def load(ctx, name):
    # Don't open a file that doesn't exist
    if name not in file_list.file_cache:
        await ctx.send("Could not find \"{}.mp3\".".format(name))
        return
    if len(bot.voice_clients) == 0:
        await ctx.send("I have no voice chat to load into.")
        return

    await ctx.send("Will now play \"{}.mp3\".".format(name))
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./audio/{}.mp3".format(name)))
    bot.voice_clients[0].play(source)

#--------#
# delete #
#--------#
@bot.command()
async def delete(ctx, name):
    await file_list.delete_audio_file(ctx, name)

# Log in
bot.run(json.load(open("auth/discord.json", "r"))["token"])
