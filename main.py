# Import public libraries
import discord
from discord.ext import commands
import logging
import json
import re
import gtts
from gtts import gTTS
from io import BytesIO

#Import custom classes, etc
import helpers.file_list as file_list
import helpers.bark as bark
from helpers.youtube import YTDLSource
from helpers.FFmpegPCMAudio import FFmpegPCMAudio
from helpers.member_info import info
from helpers.speech_to_text import incoming_audio_handler

# Define logging
logging.basicConfig(level=logging.INFO)
# Define bot
bot = commands.Bot(command_prefix="$")

#=================#
# Define commands #
#=================#
#------------#
# join/leave #
#------------#
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
    voice_client.play(bark.normal)

    # Set up channels to listen to (only) those who have opted into voice commands
    incoming_audio_handler.init(voice_channel)

@bot.command()
async def leave(ctx):
    # Can't leave a voice channel if we're not in one...
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm already not in a voice channel.")
        return

    # TODO play exit sound, not sure how to wait for sound to finish to disconnect
    #bot.voice_clients[0].play(bark.normal, after=lambda e:
    await bot.voice_clients[0].disconnect()#)
    incoming_audio_handler.clean()

#---------------#
# listen/deafen #
#---------------#
@bot.command()
async def listen(ctx):
    my_infolette = info.get_infolette(ctx.author)
    # Inform the member if they're already being listened to for voice commands
    if my_infolette.is_using_voice_commands == True:
        await ctx.send("I'm already listening for voice commands from you.")
        return

    my_infolette.is_using_voice_commands = True
    info.add_infolette(my_infolette)
    incoming_audio_handler.on_opted_members_increased(ctx.author)
    await ctx.send("Ok, I'll start listening for voice commands from you now.")

@bot.command()
async def deafen(ctx):
    my_infolette = info.get_infolette(ctx.author)
    # Inform the member if their voice already isn't being listened to
    if my_infolette.is_using_voice_commands == False:
        await ctx.send("I'm already not listening to your voice.")
        return

    my_infolette.is_using_voice_commands = False
    info.add_infolette(my_infolette)
    incoming_audio_handler.on_opted_members_decreased(ctx.author)
    await ctx.send("Ok, I'll start not listening to your voice.")

#-----------#
# play/stop #
#-----------#
@bot.command()
async def play(ctx, url):
    # Not worth trying to play audio if not connected to a channel to play into...
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm not in a voice channel to play the Youtube link in.")
        return

    # Get Youtube video, but don't predownload it (stream=True)
    player = await YTDLSource.from_url(url, stream=True)
    bot.voice_clients[0].play(player)

@bot.command()
async def stop(ctx):
    # You want me to stop... nothing? Ok... done?
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm not in a voice channel, I have nothing to stop doing.")
        return

    await bot.voice_clients[0].stop()

#----------------------------------#
# tts/tts_name/tts_lang/tts_accent #
#----------------------------------#
@bot.command()
async def tts(ctx, *, arg):
    # Not worth trying to play audio if not connected to a channel to play into...
    if len(bot.voice_clients) == 0:
        await ctx.send("I'm not in a voice channel, I have nowhere to speak.")
        return

    mp3 = BytesIO()
    member_preferences = info.get_infolette(ctx.author)
    if member_preferences.tts_accent != None:
        gTTS(text=(member_preferences.spoken_name + ": " + arg), \
            lang=member_preferences.tts_lang, \
            tld=member_preferences.tts_accent).write_to_fp(mp3)
    else:
        gTTS(text=(member_preferences.spoken_name + ": " + arg), \
            lang=member_preferences.tts_lang).write_to_fp(mp3)
    mp3.seek(0)
    # Use custom FFmpegPCMAudio class, copied from Armster15
    source = discord.PCMVolumeTransformer(FFmpegPCMAudio(mp3.read(), pipe=True))
    bot.voice_clients[0].play(source)

@bot.command()
async def tts_name(ctx, name):
    # TODO Regex for if name is reasonable?
    # Can't really do that for multi-language, just check length?
    my_infolette = info.get_infolette(ctx.author)
    my_infolette.spoken_name = name
    # Inform the member if they're already called by their desired name for TTS
    if info.add_infolette(my_infolette) == False:
        await ctx.send("I already call you " + name + " in TTS.")
        return

    await ctx.send("Ok, when doing TTS for you I'll now call you '" + name + "'.")

@bot.command()
async def tts_lang(ctx, lang):
    # If Google doesn't have an AI trained for TTS in this language, I sure don't!
    if lang not in gtts.lang.tts_langs():
        response = "I'm sorry, I don't support " + lang + ". Here's what I do support:\n"
        response += "https://en.wikipedia.org/wiki/IETF_language_tag\n"
        for code in gtts.lang.tts_langs():
            response += code + " "
        await ctx.send(response)
        return

    my_infolette = info.get_infolette(ctx.author)
    my_infolette.tts_lang = lang
    # Inform the member if they're already using their desired TTS language
    if info.add_infolette(my_infolette) == False:
        await ctx.send("I already use " + lang + " for your TTS.")
        return

    await ctx.send("Ok, I'll use " + lang + " for your TTS.")

@bot.command()
async def tts_accent(ctx, accent=None):
    my_infolette = info.get_infolette(ctx.author)
    my_infolette.tts_accent = accent
    # Inform the member if they're already using their desired TTS accent
    if info.add_infolette(my_infolette) == False:
        await ctx.send("I already the accent " + (accent if accent != None else "NONE") + " for your TTS.")
        return

    await ctx.send("Ok, I'll try to use the accent " + (accent if accent != None else "NONE") + " for your TTS. \
If it doesn't work, reissue $tts_accent with no accent. You can find available accents here: \
https://gtts.readthedocs.io/en/latest/module.html#localized-accents")

#---------------------------#
# list/save/load/delete/get #
#---------------------------#
# TODO right now it's listing all files not just mp3s?
@bot.command()
async def list(ctx):
    # Put all the mp3 files in the sound bank into a string of a index-labelled list
    full_message = "```\n"
    for i in range(len(file_list.file_cache)):
        full_message += str(i) + ". " + file_list.file_cache[i] + "\n"
    full_message += "```"

    await ctx.send(full_message)

@bot.command()
async def save(ctx):
    # Warn the user if they forgot an attachment
    if len(ctx.message.attachments) == 0:
        await ctx.send("You didn't give me an attachment to save.")
        return

    for attachment in ctx.message.attachments:
        await ctx.send("Processing \"{}\"...".format(attachment.filename))
        await file_list.save_audio_file(ctx, attachment)

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

@bot.command()
async def delete(ctx, name):
    await file_list.delete_audio_file(ctx, name)

@bot.command()
async def get(ctx, name):
    mp3_name = file_list.get_mp3_name(name)
    # Don't get a file that doesn't exist
    if mp3_name == None:
        await ctx.send("Could not find \"{}.mp3\".".format(name))
        return

    file_handle = open("./audio/{}".format(mp3_name), "rb")
    await ctx.send(file=discord.File(file_handle))

#========#
# LOG IN #
#========#
bot.run(json.load(open("auth/discord.json", "r"))["token"])
