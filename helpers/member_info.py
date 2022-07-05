# Import public libraries
import discord
import json

class MemberInfolette:
    # member should be a discord.member or a discord.member.id
    def __init__(self, \
            member, \
            spoken_name=None, \
            is_using_voice_commands=0, \
            tts_lang="en", \
            tts_accent="co.uk"):
        self.id = member.id if type(member) == discord.Member else member
        if spoken_name == None:
            self.spoken_name = member.nick if type(member) == discord.Member else member.name
        else:
            self.spoken_name = spoken_name
        self.is_using_voice_commands = is_using_voice_commands
        self.tts_lang = tts_lang
        self.tts_accent = tts_accent

    # TODO Do I need this or will 'if X in Y work'?
    def is_exact_match(self, c):
        if c.id          == self.id and \
           c.spoken_name == self.spoken_name and \
           c.is_using_voice_commands == self.is_using_voice_commands and \
           c.tts_lang    == self.tts_lang and \
           c.tts_accent  == self.tts_accent:
            return True
        return False

    def debug(self):
        print("{}: {} {} {} {}".format(self.id, \
            self.spoken_name, self.is_using_voice_commands, self.tts_lang, self.tts_accent))

    def to_json(self):
        return {\
            'id': self.id, \
            'spoken_name': self.spoken_name, \
            'is_using_voice_commands': self.is_using_voice_commands, \
            'tts_lang': self.tts_lang, \
            'tts_accent': self.tts_accent}

class MemberInfo:
    def __init__(self):
        # Recall and load previous session into memory
        self.participants = []
        previous_session = json.load(open("helpers/member_info.json", "r"))
        for participant in previous_session:
            self.participants.append(MemberInfolette(\
                participant["id"], \
                participant["spoken_name"], \
                participant["is_using_voice_commands"], \
                participant["tts_lang"], \
                participant["tts_accent"]))
        # Print list to bot owner to make sure everything is in order
        for participant in self.participants:
            participant.debug()

    # Returns the member_infolette coressponding to the passed in user,
    # if one isn't found, returns an infolette with default parameters
    # (returns a copy instead of a reference to the original)
    def get_infolette(self, member):
        match = MemberInfolette(member)
        for participant in self.participants:
            if participant.id == member.id:
                match.id          = participant.id
                match.spoken_name = participant.spoken_name
                match.is_using_voice_commands = participant.is_using_voice_commands
                match.tts_lang    = participant.tts_lang
                match.tts_accent  = participant.tts_accent
        return match

    # Attempts to add a new infolette to participants, returns true if added or modified,
    # false if matching infolette already found
    def add_infolette(self, new_infolette):
        # Case: exact infolette for member already exists, do nothing
        for participant in self.participants:
            if participant.is_exact_match(new_infolette):
                return False
        # Case: infolette for member exists, but is slightly different, overwrite
        for i in range(len(self.participants)):
            if self.participants[i].id == new_infolette.id:
                self.participants[i] = new_infolette
                self.save()
                return True
        # Case: no infolette for member exists, add one
        self.participants.append(new_infolette)
        self.save()
        return True

    # Attempts to remove the passed in infolette, returns true if deleted,
    # false if it weas not found so it could not be deleted
    def remove_infolette(self, infolette):
        for i in range(len(self.participants)):
            if self.participants[i].is_exact_match(infolette):
                self.participants.pop(i)
                self.save()
                return True
        return False

    # Returns an array of all Members who have opted into using voice commands
    def get_voice_participants(self):
        match = []
        for participant in self.participants:
            if participant.is_using_voice_commands:
                match += participant.id
        return match

    # Overwrites previous member_info.json with new self.participants JSON
    def save(self):
        result = []
        for participant in self.participants:
            result.append(participant.to_json())

        json.dump(result, open("helpers/member_info.json", "w"))

# Create common instance
# I plan to only support once voice_client and guild at a time
info = MemberInfo()
