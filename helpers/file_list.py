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
# If it exists, get the coressponding mp3 file for the name/index
# {name}.mp3
#
def get_mp3_name(name):
    # If an index was requested
    if re.fullmatch("[0-9]+", name) != None:
        if int(name) < len(file_cache):
            return file_cache[int(name)] + ".mp3"
    # If .mp3 is already in the string
    elif name.endswith(".mp3") == True:
        if name[:-4] in file_cache:
            return name
    # If a text name was requested
    elif name in file_cache:
        return name + ".mp3"

    return None

#
# Attempt to save an Attachment to our audio folder
#
async def save_audio_file(ctx, attachment):
    name = attachment.filename
    # Make name could not be confused for index
    if re.fullmatch("[0-9]+", name) != None:
        await ctx.send("Its file name would be mistaken for an index, type out a portion?")
        return False
    # Make sure the name has no suspicious characters in it
    if is_acceptable_file_name(name) == False:
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
    if get_mp3_name(name) != None:
        await ctx.send("There is already a file with that name.")
        return False

    # All is well, save into the audio folder and cache name into possible voice chat commands
    await attachment.save("./audio/{}".format(name))
    file_cache.append(name[:-4])
    await ctx.send("Succesfully saved!")
    return True

#
# Attempt delete file matching name
# {name}.mp3
#
async def delete_audio_file(ctx, name):
    mp3_name = get_mp3_name(name)
    # Don't delete a file that doesn't exist
    if mp3_name == None:
        await ctx.send("I could not find the file you want deleted.")
        return False

    os.remove("./audio/{}".format(mp3_name))
    file_cache.remove(mp3_name[:-4])
    await ctx.send("Deleted {}.".format(mp3_name))
    return True
