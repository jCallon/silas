# Silas
> Hello, I am Silas, the bot who listens!

## Basic Usage
Join a guild voice channel. From a guild text channel, send `$join`. From here, all commands can be done from DMs, and are encouraged to to avoid clutter.

### Playing sounds
- To play a Youtube link, type `$play [YouTube link]`.
- To browse the custom sound library, type `$list`. You can interact with it with `$save`, `$load`, `$get`, and `$delete`.
- Stop a sound any time with `$stop`.

### TTS
- To say anything, just type `$tts [anything]`.
- To change your preferences, there's `$tts_name`, `$tts_lang`, and `$tts_accent`.

### Using voice commands
- To respect privacy, Silas will not listen to you unless you opt in to be listened to. Enable or disable listening with `$listen` and `$deafen`.
- Actually getting voice commands to work is a WIP.

## Running Silas
- Get a discord bot token: 
  - Creating a bot account: https://docs.pycord.dev/en/master/discord.html
  - A primer to Gateway intents: https://docs.pycord.dev/en/master/intents.html
- Put your Discord bot token into `auth/discord.json`
- Install the dependancies in `requirements.txt`
- From within the virtual environment of the previous setup, run `python3 main.py`

## Bug reporting & feature requests
If you find a bug in an implemented command or would like to request a new planned command, please file an Issue and label it appropriately.

## Full command list
| Name        | Syntax                       | Description |
| ----------- | ---------------------------- | ----------- |
| join        | `$join`                      | Join requester's current guild voice chat. |
| leave       | `$leave`                     | Leave voice chat. |
| stop        | `$stop`                      | Stop playing current audio. |
| save        | `$save`                      | Save mp3 attached to message into audio bank. |
| load        | `$load "[mp3 name/index]"`   | Play `[mp3 name].mp3` or index from audio bank into voice chat. |
| get         | `$get "[mp3 name/index]"`    | Receive `[mp3 name].mp3` or index from audio bank as attachment. |
| list        | `$list`                      | List all files names and indexes in audio bank. |
| delete      | `$delete "[mp3 name/index]"` | Delete `[mp3 name].mp3` or index from audio bank. |
| play        | `$play [YouTube link]`       | Play YouTube link in voice chat. To look for title wrap in "". |
| tts         | `$tts [text]`                | Say "[your name]: [text]" in voice chat. |
| tts\_name   | `$tts_name "[name]"`         | Change the name TTS refers to you by. |
| tts\_lang   | `$tts_lang [IETF code]`      | Change your TTS language to [IETF code]. |
| tts\_accent | `$tts_accent [tld]`          | Change your TTS accent to [tld]. |
| listen      | `$listen`                    | Let bot listen to you for voice commands. |
| deafen      | `$deafen`                    | Do not let bot listen to your voice. This is default. |
