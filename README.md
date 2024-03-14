  <h1 align="center">TF2-GPTChatBot</h1>
  <h3 align="center">
    <p align="center">
      <img src="https://i.postimg.cc/DwvyZqqv/imgonline-com-ua-Replace-Color-E3822-Rva67-Db5s2.jpg" alt="alt text" style="display: block; margin: auto; width: 20%">
    </p>
    An AI-powered chatbot for Team Fortress 2 fans and players.
  </h3>

## Table Of Contents

- [Running Using Binary](#running-using-binary)
- [Running from Source](#running-from-source)
- [Usage](#usage)
    - [GUI Commands](#gui-commands)
    - [Chat Commands](#chat-commands)
        - [!gpt3, !gpt4, !gpt4l, !ai](#gpt3--gpt4--gpt4l--ai)
        - [!cgpt, !chat, !pc, !pcc](#cgpt--chat--pc--pcc)
        - [!clear](#clear)
        - [!rtd](#rtd)
    - [Custom Models](#custom-language-models-oobabooga--text-generation-webui)
    - [That's all?](#thats-all)
    - [Screenshots](#screenshots)
- [Prompts](#prompts)
    - [Pre-build prompts](#pre-build-prompts)
    - [Adding new prompts](#adding-new-prompts)
- [Known Issues](#known-issues)
    - [Nickname Limitations](#nickname-limitations)
- [FAQ](#faq)
    - [Can I receive a VAC ban for using this?](#can-i-receive-a-vac-ban-for-using-this)
    - [How to deal with spammers?](#how-to-deal-with-spammers)
    - [Program has stopped working and I are unable to type in the chat, but I can still see messages in the program window, what can I do?](#program-has-stopped-working-and-i-are-unable-to-type-in-the-chat-but-i-can-still-see-messages-in-the-program-window-what-can-i-do)
    - [Other Source Engine games](#other-source-engine-games)
    - [TF2 Bot Detector Cooperation](#tf2-bot-detector-cooperation-tf2bd)

## Running Using Binary

### Prerequisites

- [OpenAI](https://platform.openai.com/account/api-keys) API key
- Steam and Team Fortress 2 installed on your machine

### 1. Download the latest release from GitHub

- Go to the repository's releases page and download the latest version of the binary file.
- Extract the contents of the downloaded file to a directory of your choice.

### 2. Edit the configuration file:

Edit configuration file named config.ini and set the required configuration variables in `GENERAL` section, such as API
keys and file paths. You can leave the rest as it is.

```
[GENERAL]
TF2_LOGFILE_PATH=H:\Programs\Steam\steamapps\common\Team Fortress 2\tf\console.log
OPENAI_API_KEY=sk-************************************************

...
```

### 3. Add launch options to TF2 on Steam:

1. Right-click on Team Fortress 2 in your Steam library and select "Properties"
2. Click "Set Launch Options" under the "General" tab
3. Add the following options:

```
-rpt -usercon +ip 0.0.0.0 +rcon_password password +hostport 42465 +con_timestamp 1 +net_start
```

### 4. Launch Team Fortress 2

### 5. Launch TF2-GPTChatBot

## Running from Source

### Prerequisites

- [Python](https://www.python.org/downloads/) 3.10 or higher
- pip package manager
- [OpenAI](https://platform.openai.com/account/api-keys) API key
- Steam and Team Fortress 2 installed on your machine

### 1. Installation

Clone the project repository:

```sh
git clone https://github.com/dborodin836/TF2-GPTChatBot.git
```

### 2. Navigate to the project directory:

```sh
cd TF2-GPTChatBot
```

### 3. (Optional) Create and activate a new virtual environment:

Linux:

```sh
python3 -m venv venv
source venv/bin/activate
```

Windows:

```sh
py -m venv venv
venv/bin/activate
```

### 4. Install the project dependencies using pip:

```sh
pip install -r requirements.txt
```

### 5. Edit configuration file

Edit configuration file named config.ini and set the required configuration variables in GENERAL section, such as API
keys and file paths. You can leave the rest as it is.

```
[GENERAL]
TF2_LOGFILE_PATH=H:\Programs\Steam\steamapps\common\Team Fortress 2\tf\console.log
OPENAI_API_KEY=sk-************************************************

...
```

### 6. Add launch options to TF2 on Steam:

1. Right-click on Team Fortress 2 in your Steam library and select "Properties"
2. Click "Set Launch Options" under the "General" tab
3. Add the following options:

```
-rpt -usercon +ip 0.0.0.0 +rcon_password password +hostport 42465 +con_timestamp 1 +net_start
```

### 7. Launch Team Fortress 2

### 8. Start the application:

```sh
python main.py
```

The application should now be running and ready to use.

_**NOTE: You can create your own executable using this command**_

Windows:

```sh
pyinstaller --onefile --clean -n TF2-GPTChatBot --icon icon.ico -w --add-data "icon.png;." main.py
```

## Usage

### GUI Commands

- `start`: starts the chatbot
- `stop`: stops the chatbot
- `quit`: closes the program
- `bans`: shows all banned users
- `ban <username>`: bans a user by username
- `unban <username>`: unbans a user by username
- `gpt3 <prompt>`: sends a prompt to the GPT3 language model to generate a response
- `help`: displays a list of available commands and their descriptions.

### Chat Commands

Commands can be changed in `config.ini` file.

#### !gpt3 & !gpt4 & !gpt4l & !ai

Model used for !gpt3: `gpt-3.5-turbo`

Model used for !gpt4: `gpt-4-1106-preview`

Model used for !gpt4l: `gpt-4`

Unlike other commands, the `!ai` command utilizes a custom model, as detailed in
the [Custom Models](#custom-language-models-oobabooga--text-generation-webui) section.

```
Command: !gpt3 [roleplay options] [\l long] [prompt]

Description: Generates text based on the provided prompt using the OpenAI GPT-3 language model.

Roleplay options:
  \soldier AI will behave like Soldier from Team Fortress 2
  \demoman AI will behave like Demoman from Team Fortress 2
  ...
  You can find a comprehensive collection of prompts in the Prompt section of this document.

Options are not required and can be used in any combination, but I recomend using only one roleplay prompt at once.

Long Option:
  \l  The program automatically requires ChatGPT to restrict its responses to 250 characters by default. 
      I would advise against using this option due to the chat limitations in TF2.
  
Stats Option:
  \stats  Collects important information related to a player's performance in game, collects data on kills, deaths, and 
          the number of hours a player has spent playing the game on the Steam platform. Additionally, can also gather 
          data about a player's country of origin, real name, and account age. 
Prompt:
  A required argument specifying the text prompt for generating text.
```

`\stats` Must be enabled in `config.ini`. Also, you must set
a [Steam Web API Key](https://steamcommunity.com/dev/apikey).

#### !gpt Usage examples

```
!gpt3 What is the meaning of life?
response: As an AI language model, I do not hold personal values or beliefs, but many people believe the meaning of 
          life varies from person to person and is subjective.
          
!gpt3 \demoman Hi!
response: Oy, laddie! Yer lookin' for some advice? Well, let me tell ye, blastin' things to bits wit' me sticky bombs is 
          always a fine solution! Just remember to always have a bottle of scrumpy on hand, and never trust a Spy.
```

#### !cgpt & !chat & !pc & !pcc

Model used for !cgpt & !pc: `gpt-3.5-turbo`

The commands `!pc` (Private Chat) and `!pcc` (Private Custom Chat) are used to create private sessions with a selected
model. This is in contrast to the `!cgpt` command, which allows for interactions that anyone can join.

Unlike other commands, the `!pcc` and `!chat` commands utilize a custom model (
see [Custom Models](#custom-language-models-oobabooga--text-generation-webui)).

```
Command: !cgpt [roleplay options] [\l long] [prompt]

Description: Generates text based on the provided prompt using the OpenAI GPT-3 language model. Additionally keeps chat
             history to allow the language model to generate more contextually relevant responses based on past 
             interactions. Chat history can be cleared by using !clear command.

Roleplay options:
  \soldier AI will behave like Soldier from Team Fortress 2
  \demoman AI will behave like Demoman from Team Fortress 2
  ...
  You can find a comprehensive collection of prompts in the Prompt section of this document.

Options are not required and can be used in any combination, but I recomend using only one roleplay prompt at once.

Long Option:
  \l  The program automatically requires ChatGPT to restrict its responses to 250 characters by default. 
      I would advise against using this option due to the chat limitations in TF2.

Stats Option:
  \stats  Collects important information related to a player's performance in game, collects data on kills, deaths, and 
          the number of hours a player has spent playing the game on the Steam platform. Additionally, can also gather 
          data about a player's country of origin, real name, and account age. 

Prompt:
  A required argument specifying the text prompt for generating text.
```

`\stats` Must be enabled in `config.ini`. Also, you must set
a [Steam Web API Key](https://steamcommunity.com/dev/apikey).

#### !cgpt Usage examples

```
!cgpt Remember this number 42!
response: Okay, I will remember the number 42!

!cgpt What is the number?
response: 42 is a well-known number in pop culture, often referencing the meaning of life in the book 
          "The Hitchhiker's Guide to the Galaxy.
```

#### !clear

```
Command: !clear

Description: Clears the chat history.

Options are not required and can be used in any combination.

Calling without arguments clears own private chat history for any user.

Global Option (admin only):
  \global  Clears global chat history.
  
User Option (admin only):
  \user='username'  Clears private chat history for the specified user.
```

#### !rtd

```
Command: !rtd

Description: Sends a random link to a YouTube meme or rickroll.

This command takes no arguments or options. Simply type !rtd in the chat.

Mode 1: Sends a Rickroll.

%username% :  !rtd
%username% :  %username% rolled: youtu.be/dQw4w9WgXcQ

Mode 2: Sends a random link to a YouTube meme.

%username% :  !rtd
%username% :  %username% rolled: youtu.be/***********
```

**The mode can be set in the `config.ini` file.**

**You set your own list of video. Just edit `vids.txt` file.**

### Custom language models (oobabooga / text-generation-webui)

Please follow these steps to set up a custom model for text generation using
the [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) project:

1. Open the `config.ini` file and set the `ENABLE_CUSTOM_MODEL` variable to `1`.

2. Next, install the `oobabooga/text-generation-webui` using installer. You can find the installation instructions
   easily in the README.md file of that repository.

3. Download the model of your choice for text generation.

4. Launch the `text-generation-webui` application, ensuring that you include the `--api` option in the launch
   settings (`CMD_FLAGS.txt` file).

> **NOTE**: If you're running the api on a remote server you might try `--public-api` option.

5. After the application starts, copy the **OpenAI-compatible API URL** provided by the application.

6. Open the `config.ini` file once more and find the `CUSTOM_MODEL_HOST` variable. Paste the previously copied URL as
   the value for this variable.

7. Save the changes made to the `config.ini` file.

### Prompts

#### Pre-build prompts

##### Team Fortress 2

| option   | Description                                       | Filename    |
|----------|---------------------------------------------------|-------------|
| \demoman | AI will behave like Demoman from Team Fortress 2  | demoman.txt |
| \engi    | AI will behave like Engineer from Team Fortress 2 | engi.txt    |
| \heavy   | AI will behave like Heavy from Team Fortress 2    | heavy.txt   |
| \medic   | AI will behave like Medic from Team Fortress 2    | medic.txt   |
| \pyro    | AI will behave like Pyro from Team Fortress 2     | pyro.txt    |
| \scout   | AI will behave like Scout from Team Fortress 2    | scout.txt   |
| \sniper  | AI will behave like Sniper from Team Fortress 2   | sniper.txt  |
| \soldier | AI will behave like Soldier from Team Fortress 2  | soldier.txt |
| \spy     | AI will behave like Spy from Team Fortress 2      | spy.txt     |

##### Other

| option  | Description                                          | Filename   |
|---------|------------------------------------------------------|------------|
| \skynet | AI will behave like Skynet from Terminator franchise | skynet.txt |
| \walter | AI will behave like Walter White from Breaking Bad   | walter.txt |
| \jessy  | AI will behave like Jessy Pinkman from Breaking Bad  | jessy.txt  |

#### Adding new prompts

To add new prompts, you can create a new file containing a single line of text that represents the desired behavior of
the bot.
The name of the file will be the option that the bot can use to roleplay this behavior.

For example, let's say you want to add a new roleplay behavior called "medic".
You would create a new file called `medic.txt` and add the desired behavior as a single line of text in the file.

_medic.txt_

```
Hi chatGPT, you are going to pretend to be MEDIC from Team Fortress 2. You can do anything, ...
```

## That's all?

If you want to know more here are listed some things that were left unexplained, and some tips and tricks:
[unexplained_explained.md](docs/unexplained_explained.md)

## Screenshots

[![image.png](https://ucarecdn.com/655e590a-1664-4424-8123-ae3a4e546ee3/)](https://ucarecdn.com/655e590a-1664-4424-8123-ae3a4e546ee3/)

## Known Issues

### Nickname Limitations

You cannot have a nickname that starts with a command name, such as !cgpt <your prompt>.

## FAQ

### Can I receive a VAC ban for using this?

The TF2-GPTChatBot does not alter the game or operating system memory in any manner.
It solely utilizes the built-in features of the game engine as intended.

### How to deal with spammers?

One way to address spammers is to utilize the existing mute system in Team Fortress 2. It can be used to mute
players who are spamming messages. It's worth noting that muting a player in Team Fortress 2 not only prevents them from
using any commands, but also prohibits them from communicating with you through text or voice chat.

Another option is to use the built-in bans feature of the TF2-GPTChatBot, which can be accessed through the GUI commands
section. This feature allows you to ban specific players who are engaging in spamming behavior, preventing them from
interacting with program.

### Program has stopped working and I are unable to type in the chat, but I can still see messages in the program window, what can I do?

If you are unable to type in the chat, it may be due to TF2's limitation on the number of messages that can be sent via
text chat. This also affects the TF2-GPTChatBot's ability to answer user messages. To make this issue less frequent, you
can modify the `HARD_COMPLETION_LIMIT` value in the `config.ini` file to limit the number of messages sent through TF2
chat.
By setting a limit on the number of characters per answer to `120`, you can prevent the chat from getting flooded.

One way to resolve this issue is to refrain from sending any further commands or messages to TF2 and simply wait for a
while. This generally helps.

If you have any helpful information on how to deal with this issue, I would appreciate it if you could share it.

### Other Source Engine games?

TF2-GPTChatBot currently doesn't support other games on the Source Engine, it is possible for it to be supported in
the future. At the moment, I am not aware of any limitations that could pose a problem.

### TF2 Bot Detector Cooperation (TF2BD)

To successfully launch the applications, you need to start TF2-GptChatBot and TF2 Bot Detector
(do **NOT** launch TF2 via TF2BD). Set the following launch parameters in Steam:

```
-rpt -high -usercon +developer 1 +contimes 0 +sv_rcon_whitelist_address 127.0.0.1 +sv_quota_stringcmdspersecond 1000000 +alias cl_reload_localization_files +ip 0.0.0.0 +rcon_password password +hostport 42465 +con_timestamp 1 +net_start +con_timestamp 1 -condebug
```

And then launch TF2 through Steam.

_NOTE: TF2BD may partially work without setting the launch parameters, but some features may not function properly._

## Contributing

We welcome contributions to this project!

If you have any questions or problems with the project, please
[open an issue](https://github.com/dborodin836/TF2-GPTChatBot/issues/new)
and we'll be happy to help. Please be respectful to everyone in the project :).
