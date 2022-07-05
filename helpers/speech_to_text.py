# Import public libraries
import discord
import speech_recognition as gSST

#Import custom classes, etc
import helpers.bark
from helpers.member_info import info

keyword = "pup"

#----------#
# Overview #
#----------#
# Once voice chat is joined, for each opted in voice chat member:
# . Put listeners up for when they are speaking
# . When they are speaking, listen to the 1st second only
#   . If they said keyword and nothing else:
#     . Bark to let the member know they've started voice command recognition
#     . Listen to the user for a command the next time they speak
#     . Bark to let the member know Silas has ended voice command recognition
#     . Parse the audio into a command
#       . If the command is recognized, try running it
#         . If the command was successful, no followup is needed
#         . Else tell the member the command failed and Silas DMed them why
#       . Else tell the member the command is not recognised

#------------------------------------------------------#
# For each opted-in member connected to voice_channel, #
# have a MemberStream to listen for changes in their   #
# voice state and dispatch audio recorders             #
#------------------------------------------------------#

class MemberStream:
    def __init__(self, member, voice_channel):
        self.id = member.id
        self.voice_channel = voice_channel
        #self.speaking_event_listener = #discord voice states do not include currently speaking, will need some nerding with the socket directly?
        self.expecting_command = False

    # I can increase time and call this on a loop if I need a workaround for detecting when a memver is speaking
    def on_member_speaking():
        sink = discord.WaveSink(users=self.id, time=1)
        if self.expecting_command:
            sink.filters.time = 10
        self.voice_channel.start_recording(sink, parse_recording, None)

    def on_member_not_speaking():
        self.voice_channel.stop_recording()

#------------------------------------------------------#
# Manage all above MemberStreams, such as if a member  #
# joins or drops.
#------------------------------------------------------#

class MemberStreamDelegator:
    def __init__(self):
        self.clean()

    # Creates and indexes a MemberStream for each opted-in voice chat member
    def init(self, voice_channel):
        self.voice_channel = voice_channel
        self.member_streams = {}
        for member in voice_channel.members:
            if member.id in info.get_voice_participants():
                self.member_streams[member.id] = MemberStream(member)

    # Sets every member to empty, wiping state
    def clean(self):
        self.voice_channel = None
        self.member_streams = {}

    # When a member joins, create a MemberStream for them if they are opted-in
    def on_member_joined_voice_chat(member):
        if member.id in info.get_voice_participants():
            self.member_streams[member.id] = MemberStream(member)

    # When a member leaves, remove their MemberStream, if they had one
    def on_member_left_voice_chat(member):
        if member.id in self.member_streams:
            self.member_streams.pop(member.id)

    # If voice chat member opts-in mid-call, we might need to add a MemberStream for them
    def on_opted_members_increased(member):
        if self.voice_channel == None:
            return
        if member in self.voice_channel.members:
            self.member_streams[member.id] = MemberStream(member)

    # If voice chat member opts-out mid-call, we might need to remove a MemberStream for them
    def on_opted_members_decreased(member):
        if member.id in self.member_streams:
            self.member_streams.pop(member.id)

# Create common instance
incoming_audio_handler = MemberStreamDelegator()

#--------------------------------#
# Actually do things with audio! #
#--------------------------------#

command_text = {\
    "join":       "I'm already joined.",
    "leave":      "Ok, I'll leave.",
    "stop":       None,
    "save":       "Please use 'save' over DMs instead.",
    "load":       None,
    "get":        "Ok, I'll get that audio file into your DMs.",
    "list":       "Ok, I'll send a list of my audio bank to your DMs.",
    "delete":     "Please use 'delete' over DMs instead.",
    "play":       None,
    "tts":        "Please use 'tts' over DMs instead.",
    "tts_name":   "Please use 'tts_name' over DMs instead.",
    "tts_lang":   "Please use 'tts_lang' over DMs instead.",
    "tts_accent": "Please use 'tts_accent' over DMs instead.",
    "listen":     "I'm already listening to you.",
    "deafen":     "Ok, I'll stop listening to you."
}

#TODO try to make it all run in memory instead of writing to disk?
async def parse_recording(sink, channel: discord.TextChannel, *args):
    # There should only be one item (decrypted recording), because a sink is set up per member
    rec = sink.audio_data.items()
    if len(rec) != 1:
        return

    # Create discord.File object for decrypted recording, give to STT (speech-to-text) parser
    discord_file = discord.File(rec.audio.file, rec.user_id + '.' + sink.encoding)
    gSST_audio = gSST.AudioFile(discord.file_name)
    gSST_text = gSST.recognize_google(gSST_audio)
    if len(gSST_text) < 3:
        return

    # Use parsed text, can exit early if member is not in command parsing stage
    my_member_stream = my_member_stream_delegator.member_streams[rec.user_id]
    if my_member_stream.expecting_command == False:
        if gSST_text == keyword:
            voice_client.play(bark.high)
            my_member_stream.expecting_command = True
        return
    voice_client.play(bark.low)
    my_member_stream.expecting_command == False

    # Get TTS response for command
    command_name = gSST_text.split(" ")[0]
    if command_name not in command_text:
        await bot.commands.tts(ctx, "I do not know command '"+ command_name +"'.")
        return
    command_tts = command_text[command_name]
    #build fake context? pull from global variable?
    if command_tts != None:
        await bot.commands.tts(ctx, command_tts)

    # Run command, TODO make this less ugly
    command_args = gTTS_text[len(command_name):]
    if command_name == "leave":
        bot.commands.leave(ctx)
    elif command_name == "stop":
        bot.commands.stop(ctx)
    elif command_name == "load":
        bot.commands.load(ctx, command_args)
    elif command_name == "get":
        bot.commands.get(ctx, command_args)
    elif command_name == "list":
        bot.commands.list(ctx)
    elif command_name == "play":
        bot.commands.play(ctx, command_args)
    elif command_name == "deafen":
        bot.commands.deafen(ctx)
