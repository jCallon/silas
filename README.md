# Pfitzer 1.0.0
> Hello, I am Pfitzer, the bot you can hear!

After getting your own bot token, run `python main.py` to start the bot.

If you find a bug in an implemented command or would like to request a new planned command, please file an Issue.

## Implemented Commands
| Name   | Syntax                 | Description |
| ------ | ---------------------- | ----------- |
| join   | `$join`                | Join requester's current guild voice chat. |
| leave  | `$leave`               | Leave voice chat. |
| save   | `$save [attachment]`   | Save attached mp3 into audio bank. |
| load   | `$load "[mp3 name]"`   | Play `[mp3 name].mp3` from audio bank in voice chat. |
| delete | `$delete "[mp3 name]"` | Delete `[mp3 name].mp3` from audio bank. |
| stop   | `$stop`                | Stop playing current audio. |

## Planned Commands
| Name   | Syntax                 | Description |
| ------ | ---------------------- | ----------- |
| play   | `$play [YouTube link]` | Play YouTube link in voice chat. |
| leave  | `$list`                | List all files in audio bank. |
| leave  | `$get "[mp3 name]"`    | Receive [mp3 name].mp3 from audio bank as attachment. |
| tts    | `$tts [text]`          | Say [text] in voice chat. |
| lang   | `$lang [IETF code]`    | Set your desired language for TTS. |
| listen | `$listen`              | Let bot listen to you for voice commands. |
| ignore | `$ignore`              | Do not let bot listen to you. This is default. |
| toggle | `$toggle "[mp3 name]"` | Toggle if [mp3 name].mp3 can be invoked by voice command. |