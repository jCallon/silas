# Silas
> Hello, I am Silas, the bot who listens!

## Usage
Join a guild voice channel. From a guild text channel, send `$join`. From here, all commands can be done from DMs, and are advised to be to avoid clutter.

### Playing sounds
- To play a Youtube link, type `$play [YouTube link]`.
- To browse the custom sound library, type `$list`. You can interact with it with `$save`, `$load"`, `$get`, and `$delete`.
- Stop a sound any time with `$stop`.

### TTS
- To say anything, just type `$tts [anything]`.
- To change your preferences, there's `$tts_name`, `$tts_lang`, and `$tts_accent`.

### Using voice commands
- To respect privacy, Silas will not listen to you unless you opt in to be listened to. Enable or disable listening with `$listen` and `$deafen`.
- Actually getting voice commands to work is a WIP.

## Running Silas
I NEED TO UPDATE THIS - see requirements.txt
After getting your own Discord bot token and making the code point at it, run `python3 main.py` to start the bot. To get the dependancies it'll complain about I recommend...
1. Make a virtual environment: `python3 -m venv bot-env`
2. Activate virtual environment: Linux `source bot-env/bin/activate`, Windows `bot-env\Scripts\activate.bat`
3. Install dependancies: `pip install -U ...`
- `discord.py`
- `discord.py[voice]`
- `youtube_dl`
4. Install `ffmpeg` somewhere, I forget how.

## Bug reporting & feature requests
If you find a bug in an implemented command or would like to request a new planned command, please file an Issue and label it appropriately.

## Full command list
| Name   | Syntax                       | Description |
| ------ | ---------------------------- | ----------- |
| join   | `$join`                      | Join requester's current guild voice chat. |
| leave  | `$leave`                     | Leave voice chat. |
| stop   | `$stop`                      | Stop playing current audio. |
| save   | `$save`                      | Save mp3 attached to message into audio bank. |
| load   | `$load "[mp3 name/index]"`   | Play `[mp3 name].mp3` or index from audio bank into voice chat. |
| get    | `$get "[mp3 name/index]"`    | Receive `[mp3 name].mp3` or index from audio bank as attachment. |
| list   | `$list`                      | List all files names and indexes in audio bank. |
| delete | `$delete "[mp3 name/index]"` | Delete `[mp3 name].mp3` or index from audio bank. |
| play   | `$play [YouTube link]`       | Play YouTube link in voice chat. |
| tts    | `$tts [text]`                | Say "[your name]: [text]" in voice chat. |
| tts    | `$tts_name [preferred name]` | Change the name TTS refers to you by. |
| tts    | `$tts_lang [IETF code]`      | Change your TTS language to [IETF code]. |
| tts    | `$tts_accent [tld]`          | Change your TTS accent to [tld]. |
| listen | `$listen`                    | Let bot listen to you for voice commands. |
| deafen | `$deafen`                    | Do not let bot listen to your voice. This is default. |
