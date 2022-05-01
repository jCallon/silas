# Silas
> Hello, I am Silas, the bot who listens!

After getting your own bot token, run `python main.py` to start the bot.

If you find a bug in an implemented command or would like to request a new planned command, please file an Issue.

## Implemented Commands
| Name   | Syntax                       | Description |
| ------ | ---------------------------- | ----------- |
| join   | `$join`                      | Join requester's current guild voice chat. |
| leave  | `$leave`                     | Leave voice chat. |
| stop   | `$stop`                      | Stop playing current audio. |
| save   | `$save [attachment]`         | Save attached mp3 into audio bank. |
| load   | `$load "[mp3 name/index]"`   | Play `[mp3 name].mp3` or index from audio bank into voice chat. |
| get    | `$get "[mp3 name/index]"`    | Receive `[mp3 name].mp3` or index from audio bank as attachment. |
| list   | `$list`                      | List all files names and indexes in audio bank. |
| delete | `$delete "[mp3 name/index]"` | Delete `[mp3 name].mp3` or index from audio bank. |

## Planned Commands
| Name   | Syntax                       | Description |
| ------ | ---------------------------- | ----------- |
| play   | `$play [YouTube link]`       | Play YouTube link in voice chat. |
| tts    | `$tts [text]`                | Say [text] in voice chat. |
| lang   | `$lang [IETF code]`          | Set your desired language for TTS. |
| listen | `$listen`                    | Let bot listen to you for voice commands. |
| ignore | `$ignore`                    | Do not let bot listen to your voice. This is default. |
| toggle | `$toggle "[mp3 name/index]"` | Toggle if `[mp3 name].mp3` can be invoked by voice command. |
