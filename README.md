  <h1 align="center">TF2-GPTChatBot</h1>
  <h3 align="center">
    <p align="center">
      <img src="https://i.postimg.cc/DwvyZqqv/imgonline-com-ua-Replace-Color-E3822-Rva67-Db5s2.jpg" alt="alt text" style="display: block; margin: auto; width: 20%">
    </p>
    An AI-powered chatbot for Team Fortress 2 fans and players.
  </h3>

## TF2-GPTChatBot Installation Guide

## Table Of Contents

- [Running Using Binary](#running-using-binary)
- [Running from Source](#running-from-source)
- [Usage](#usage)
    - [Commands](#comands)
        - [!gpt3](#-gpt3)
        - [!cgpt](#-cgpt)
        - [!clear](#-clear)
    - [Screenshots](#screenshots)
- [Prompts](#prompts)
    - [Pre-build prompts](#pre-build-prompts)
    - [Adding new prompts](#adding-new-prompts)
- [FAQ](#faq)
    - [Can I receive a VAC ban for using this?](can-i-receive-a-VAC-ban-for-using-this?)

## Running Using Binary

### Prerequisites

- [OpenAI](https://platform.openai.com/account/api-keys) API key
- Steam and Team Fortress 2 installed on your machine

### 1. Download the latest release from GitHub

- Go to the repository's releases page and download the latest version of the binary file.
- Extract the contents of the downloaded file to a directory of your choice.

### 2. Edit the configuration file:

Edit configuration file named config.ini and set the required configuration variables in GENERAL section, such as API
keys and file paths. You can leave the rest as it is.

Here's an example of what the config file might look like:

```
[GENERAL]
TF2_LOGFILE_PATH=C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\console.log
OPENAI_API_KEY=sk-blahblahblahblahblahblahblahblahblahblahblahblah

[COMMANDS]
GPT_COMMAND=!gpt3
CHATGPT_COMMAND=!cgpt
CLEAR_CHAT_COMMAND=!clear

[RCON]
RCON_HOST=127.0.0.1
RCON_PASSWORD=password
RCON_PORT=27015

[MISC]
SOFT_COMPLETION_LIMIT=128
HARD_COMPLETION_LIMIT=300
```

### 3. Add launch options to TF2 on Steam:

1. Right-click on Team Fortress 2 in your Steam library and select "Properties"
2. Click "Set Launch Options" under the "General" tab
3. Add the following options:

```
-rpt -usercon -ip 0.0.0.0 +rcon_password password +net_start
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

Here's an example of what the config file might look like:

```
[GENERAL]
TF2_LOGFILE_PATH=C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\console.log
OPENAI_API_KEY=sk-blahblahblahblahblahblahblahblahblahblahblahblah

[COMMANDS]
GPT_COMMAND=!gpt3
CHATGPT_COMMAND=!cgpt
CLEAR_CHAT_COMMAND=!clear

[RCON]
RCON_HOST=127.0.0.1
RCON_PASSWORD=password
RCON_PORT=27015

[MISC]
SOFT_COMPLETION_LIMIT=128
HARD_COMPLETION_LIMIT=300
```

### 6. Add launch options to TF2 on Steam:

1. Right-click on Team Fortress 2 in your Steam library and select "Properties"
2. Click "Set Launch Options" under the "General" tab
3. Add the following options:

```
-rpt -usercon -ip 0.0.0.0 +rcon_password password +net_start
```

### 7. Launch Team Fortress 2

### 8. Start the application:

```sh
python main.py
```

The application should now be running and ready to use.

## Usage

### Commands

Commands can be changed in `config.ini` file.

#### !gpt3

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
  
Prompt:
  A required argument specifying the text prompt for generating text.
```

#### !gpt3 Usage examples

```
!gpt3 What is the meaning of life?
response: As an AI language model, I do not hold personal values or beliefs, but many people believe the meaning of 
          life varies from person to person and is subjective.
          
!gpt3 \demoman Hi!
response: Oy, laddie! Yer lookin' for some advice? Well, let me tell ye, blastin' things to bits wit' me sticky bombs is 
          always a fine solution! Just remember to always have a bottle of scrumpy on hand, and never trust a Spy.
```

#### !cgpt

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
  
Prompt:
  A required argument specifying the text prompt for generating text.
```

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

This command takes no arguments or options. Simply type !clear in the chat to clear the history. Be careful, this action 
cannot be undone.
```

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

### Screenshots

## FAQ

### Can I receive a VAC ban for using this?

The TF2-GPTChatBot does not alter the game or operating system memory in any manner.
It solely utilizes the built-in features of the game engine as intended.
