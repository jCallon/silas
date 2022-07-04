# Import libraries
import discord
from discord.ext import commands
import logging
import json
import re
from gtts import gTTS
from io import BytesIO

#Import files
import file_list
from youtube import YTDLSource
from FFmpegPCMAudio import FFmpegPCMAudio

# Define logging
logging.basicConfig(level=logging.INFO)
# Define bot
bot = commands.Bot(command_prefix="$")

#=================#
# Define commands #
#=================#
# Note: I plan to only support once voice_client at a time
#------#
# join #
#------#
@bot.command()
async def join(ctx):
    # Author must have a voice connection to join
    if type(ctx.author) != discord.Member or ctx.author.voice == None:
        await ctx.send("You must be in a guild voice chat and use $join from a guild text chat.")
        return
    # If in a voice channel already, leave it
    if len(bot.voice_clients) != 0:
        await leave(ctx)

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./bark.mp3"))
    voice_client.play(source)

#-------#
# leave #
#-------#
@bot.command()
async def leave(ctx):
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm already not in a voice channel.")
        return

    # TODO play exit sound, not sure how to wait for sound to finish to disconnect
    #source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./bark.mp3"))
    #bot.voice_clients[0].play(source, after=lambda e:
    await bot.voice_clients[0].disconnect()#)

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
@bot.command()
async def play(ctx, url):
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm not in a voice channel to play the Youtube link in.")
        return

    # Get Youtube video, but don't predownload it (stream=True)
    player = await YTDLSource.from_url(url, stream=True)
    bot.voice_clients[0].play(player)

#-----#
# tts #
#-----#
@bot.command()
async def tts(ctx, *, arg):
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm not in a voice channel, I have nowhere to speak.")
        return

    mp3 = BytesIO()
    gTTS(text=arg, lang="en", tld="co.uk").write_to_fp(mp3)
    mp3.seek(0)
    # Use custom FFmpegPCMAudio class, copied from Armster15
    source = discord.PCMVolumeTransformer(FFmpegPCMAudio(mp3.read(), pipe=True))
    bot.voice_clients[0].play(source)

#------#
# save #
#------#
@bot.command()
async def save(ctx):
    # Warn the user if they forgot an attachment
    if len(ctx.message.attachments) == 0:
        await ctx.send("You didn't give me an attachment to save.")
        return

    for attachment in ctx.message.attachments:
        await ctx.send("Processing \"{}\"...".format(attachment.filename))
        await file_list.save_audio_file(ctx, attachment)

#------#
# load #
#------#
@bot.command()
async def load(ctx, name):
    mp3_name = file_list.get_mp3_name(name)
    # Don't open a file that doesn't exist
    if mp3_name == None:
        await ctx.send("Could not find \"{}.mp3\".".format(name))
        return
    # Tell user if there's no voice client to play into anyways
    if len(bot.voice_clients) == 0:
        await ctx.send("I have no voice chat to load into.")
        return

    await ctx.send("Will now play \"{}\".".format(mp3_name))
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./audio/{}".format(mp3_name)))
    bot.voice_clients[0].play(source)

#--------#
# delete #
#--------#
@bot.command()
async def delete(ctx, name):
    await file_list.delete_audio_file(ctx, name)

#------#
# list #
#------#
@bot.command()
async def list(ctx):
    full_message = "```\n"
    for i in range(len(file_list.file_cache)):
        full_message += str(i) + ". " + file_list.file_cache[i] + "\n"
    full_message += "```"

    await ctx.send(full_message)

#-----#
# get #
#-----#
@bot.command()
async def get(ctx, name):
    mp3_name = file_list.get_mp3_name(name)
    # Don't get a file that doesn't exist
    if mp3_name == None:
        await ctx.send("Could not find \"{}.mp3\".".format(name))
        return

    file_handle = open("./audio/{}".format(mp3_name), "rb")
    await ctx.send(file=discord.File(file_handle))

# Log in
bot.run(json.load(open("auth/discord.json", "r"))["token"])
