## Table Of Contents

- [Introduction](#Introduction)
  - [Running from Source](#running-from-source)
- [Config configurations](#Config-configurations)
  - [General](#General)
  - [Commands](#Commands)
  - [RCON](#RCON)
  - [Chat](#Chat)
  - [Misc](#Misc)
  - [Stats](#Stats)
  - [CUSTOM-MODEL-GENERAL](#CUSTOM-MODEL-GENERAL)
 - [Tips and Tricks (TEXT-GENERATION-WEBUI)](#Tips-and-Tricks-TEXT-GENERATION-WEBUI)

## Introduction 

So... You bloody self-proclaimed scientist of a merc decided to look into documentation?

Good, because there we're going to explain how to set up this abomination of a program with no proper GUI and tell some tips and tricks on how to use it! <sub>(No offense)</sub>

Yes, I know how you're feeling right now, scared, scared of all this text you have to read through, and maybe a bit excited, if you're crazy and touch grass every day. <sub>(No offense x2)</sub>

### Running from Source

- I assume that you followed the instructions on how to install the program on the main page. There is a start.bat that should make the initial install process easier, but there's a chance that it won't work.
- If it doesn't work — just manually follow the steps on the main page and you're good to go.
- If you're still stuck because of an error make sure that you have git and python installed on your machine.
- If you're STILL STUCK create an issue, and make sure that you have checked the existing closed issues that might have a solution you're looking for.
- If you successfully launched the program and see the GUI right in front of you, congratulations, now let's move on to the config.ini file where most of the tinkering going to happen.

## Config configurations

### General

- Change the `TF2_LOGFILE_PATH` file path to the correct one. The default path on most of the machines is:
```
TF2_LOGFILE_PATH=C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\console.log
```
- If you use OPENAI write down your API key in the respected option.

### Commands

- All the `_COMMAND` options configure the command that will trigger the AI by the users in the in-game chat.
- The `GPT4_ADMIN_ONLY` option restricts the usage of `!gpt4` commands for everyone except the host (you).
- The `_MODEL` settings are recommended to be left as is, it's the ID of the model that is going to be used.

### RCON

- Leave these settings as is. Change them only if you changed one of these settings using the TF2's launch options or autoexec.

### Chat

- Most of these are already explained in the config.ini I will touch on settings that have not yet been explained.

### Misc

- `SOFT_COMPLETION_LIMIT` adds the following string to the user message: `Answer in less than 128 chars!` It should bias the model to write less than required.
- `HARD_COMPLETION_LIMIT` will truncate the message if it exceeds the 300 chars limit and add "..." at the end of the response. Note that this doesn't truncate the actual AI's message but only the message that is being sent to TF2. Further in the tutorial, I will explain how to truncate the message.
- `TOS_VIOLATION` Affects only !gpt commands. It will ignore all the prompts that violate OPENAI's Terms Of Service.

### Stats

- By enabling stats and setting your `STEAM_WEBAPI_KEY` you will be able to use the \stats flag that will get the information about the current game, all the player's kills and deaths, k/d ratio, the time they are playing on the server, etc. Sadly the score is not included.

### CUSTOM-MODEL-GENERAL

- `ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL` obviously switches the soft limit on and off from its name.
- `ENABLE_CUSTOM_MODEL` whether you want to use the custom model or not.
- `CUSTOM_MODEL_COMMAND` is the command that will trigger the AI.
- `CUSTOM_MODEL_CHAT_COMMAND` is the command that will trigger the AI and its chat history.
- `GREETING` As explained in the config.ini, adds the first message as AI. Quite useful when you want the AI to speak in a specific sort of way.

The other stuff is self-explanatory or already explained.

Now let's move on to the tips and tricks.

## Tips and Tricks (TEXT-GENERATION-WEBUI)

- You can change the command to be a word, for example, you can change it to "bot" so the AI will trigger every time someone says bot. Or you can change it to a whole secret code? No practical use but funny.
- All the tinkering revolves around the `CUSTOM_MODEL_SETTINGS` To see all the settings go to the `127.0.0.1:5000/docs` it will open up the API documentation of the `text-generation-webui` and open up the `v1/chat/completions` here are all the settings.
- One of the useful settings is `preset` so you don't have to type all the settings you want manually, you can save the preset in the text-generation-webui and import it using this simple option.
- Remember I talked about truncating the actual AI's response? The setting to do it is `max_tokens`. Why would you need this if you have `HARD_COMPLETION_LIMIT`? Well when you use the `HARD_COMPLETION_LIMIT` and the user wants the AI to continue it will get confused because it already outputted the whole message, it's just the message in tf2 that got cut down. So that's why I recommend using `max_tokens` instead.
- `name1` and `name2` also could be useful, `name1` refers to `User`, while `name2` refers to `AI` (Assistant). By default the `name1` is set as "`You`" You can save the session setting in text-generation-webui so the `name1` will always be "`User`", but this might require you to reboot the WebUI, this will get annoying if you change the names a lot.
- You can change the `mode` but in my tests, the `chat` mode worked the best. May vary depending on your model, so experiment with this.
- You can also use `character` or `instruction_template`. But this also requires the WebUI to be rebooted if you modify the character's or instruction template's content, it just doesn't update, it will still use the old template for some reason. So instead of that you can type your character's context in the respected `context` setting.
