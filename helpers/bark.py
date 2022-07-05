# Import public libraries
import discord

normal = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("helpers/bark.mp3"))
high = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("helpers/high_bark.mp3"))
low = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("helpers/low_bark.mp3"))
