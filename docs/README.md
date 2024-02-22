## Table Of Contents

- [Introduction](#Introduction)
- [Install from source](#Install-from-source)
- [Config configurations](#Config-configurations)
 - [General](#General)
 - [Commands](#Commands)
 - [RCON](#RCON)
 - [Chat](#Chat)
 - [Stats](#Stats)
 - [CUSTOM-MODEL-GENERAL](#CUSTOM-MODEL-GENERAL)
 - [Tips and Tricks (TEXT-GENERATION-WEBUI)](#Tips-and-Tricks-(TEXT-GENERATION-WEBUI))

### Introduction 

So... You bloody self-proclaimed scientist of a merc decided to look into documentation?

Good, because there we're going to explain how to setup this abomination of a program with no proper GUI and teel some tips and tricks on how to use it! <sub>(No offense)</sub>

Yes, I know how you're feeling right now, scared, scared of all this text you have to read through, and maybe a bit excited, if you're crazy and touch grass everyday. <sub>(No offense x2)</sub>

### Install from source

- I assume that you followed the instructions on how to install the program on the main page. There is a start.bat that should make the initial install process easier, but there's a chance that it won't work.
- If it doesn't work — just manually follow the steps on the main page and you're good to go.
- If you're still stuck because of an error make sure that you have git and python installed on your machine.
- If you're STILL STUCK create an issue, and make sure that you have checked the existing closed issues that might have a solution you're looking for.
- If you successfully launched the program and see the GUI right infront of you, congratulations, now let's move on to the config.ini file where most of the tinkering going to happen.

## Config configurations

### General

- Change the `TF2_LOGFILE_PATH` file path to the correct one. The default path on most of the machines is:
```
TF2_LOGFILE_PATH=C:\Programs (x86)\Steam\steamapps\common\Team Fortress 2\tf\console.log
```
If you use OPENAI write down your API key in the respected option.

### Commands

- All the `_COMMAND` options configures the command that will trigger the AI by the users in the in-game chat.
- `GPT4_ADMIN_ONLY` option restricts the usage of `!gpt4` commands for everyone except the host (you).
- The `_MODEL` settings are recommended to be left as is, it's the ID of the model that is going to be used.

### RCON

- Leave these settings as is. Change them only if you changed one of these settings using the TF2's launch options or autoexec.

### Chat

- Most of these are already explained in the config.ini I will touch on settings that have not yet been explained.
- `SOFT_COMPLETION_LIMIT` adds a following string to the user message: `Answer in less than 128 chars!` It should bias the model to write less than required.
- `HARD_COMPLETION_LIMIT` will truncate the message if it exceeded the 300 chars limit and add "..." at the end of the response. Note that this don't truncate the actual AI's message but only the message that is being sent to TF2. Further in the tutorial I will explain how to truncate the actual message.
- `TOS_VIOLATION` Affects only !gpt commands. It will ignore all the prompts that violates the OPENAI's Terms Of Service.

### Stats

- By enabling stats and setting your `STEAM_WEBAPI_KEY` you will be able to use the \stats flag that will get the information about the current game, all the player's kills and deaths, k/d ratio, time they are playing on the server and etc. Sadly the score is not included.

### CUSTOM-MODEL-GENERAL

- `ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL` obvious from its name, switches the soft limit on and off.
- `ENABLE_CUSTOM_MODEL` whether you want to use the custom model or not.
- `CUSTOM_MODEL_COMMAND` the command that will trigger the AI.
- `CUSTOM_MODEL_CHAT_COMMAND` the command that will trigger the AI and its chat history.

The other stuff is self explanatory or already explained.

Now let's move on to the tips and tricks.

## Tips and Tricks (TEXT-GENERATION-WEBUI)

- You can change the command to be a word, for example you can change it to "bot" so the AI will trigger everytime someone says bot. Or you can change it to a whole secret code? No practical use but funny.
- All the tinkering revolves around the `CUSTOM_MODEL_SETTINGS` To see all the settings go to the 127.0.0.1:5000/docs it will open up the API documentation of the `text-generation-webui` open up the v1/chat/completions here are all the settings.
