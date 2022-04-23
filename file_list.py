import os
import re

#
# Set reasonable limits so no one melts my SSD/HDD...
#
max_files      = 100
max_file_bytes = 20000000 #20MB

#
# Put the names of available audio files into memory (a variable) for faster skimming
#
file_cache = os.listdir('./audio')
for i in range(len(file_cache)):
    file_cache[i] = file_cache[i][:-4]
print(file_cache)

#
# Check a file name has no malicious filesystem character and can be spoken
#
def is_acceptable_file_name(file_name):
    return re.fullmatch("[a-z 0-9]+\.mp3", file_name)

#
# Answer if we have the file
# {name}.mp3
#
def has_audio_file(name):
    if name in file_cache:
        return True
    return False

#
# Attempt to save an Attachment to our audio folder
#
async def save_audio_file(ctx, attachment):
    # Make sure the name has no suspicious characters in it
    if is_acceptable_file_name(attachment.filename) == True:
        await ctx.send("I only accept [a-z, ,0-9].mp3!")
        return False
    # Make sure we are not over the file size cap
    if attachment.size > max_file_bytes:
        await ctx.send("Over {} byte limit! Please trim/compress it.".format(max_file_bytes))
        return False
    # Make sure we are not over the file amount cap
    if len(file_cache) > max_files:
        await ctx.send("At my {} audio file limit! Delete an unneeded file.".format(max_files))
        return False
    # Make sure file name isn't already in use
    if has_audio_file(attachment.filename[:-4]) == True:
        await ctx.send("There is already a file with that name.")
        return False

    # All is well, save into the audio folder and cache name into possible voice chat commands
    await attachment.save("./audio/{}".format(attachment.filename))
    file_cache.append(attachment.filename[:-4])
    await ctx.send("Succesfully saved!")
    return True

#
# Attempt delete file matching name
# {name}.mp3
#
async def delete_audio_file(ctx, name):
    # Don't delete a file that doesn't exist
    if has_audio_file(name) == False:
        await ctx.send("Could not find {}.mp3.".format(name))
        return False

    os.remove("./audio/{}.mp3".format(name))
    file_cache.remove(name)
    await ctx.send("Deleted {}.mp3.".format(name))
    return True
