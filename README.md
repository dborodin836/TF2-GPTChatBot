  <h1 align="center">TF2-GPTChatBot</h1>
  <h3 align="center">
    <p align="center">
      <img src="https://i.postimg.cc/DwvyZqqv/imgonline-com-ua-Replace-Color-E3822-Rva67-Db5s2.jpg" alt="alt text" style="display: block; margin: auto; width: 20%">
    </p>
    An AI-powered chatbot for Team Fortress 2 fans and players.
  </h3>

> [!IMPORTANT]
> This is v2 of the chatbot, which is now in beta. v1 will be replaced by v2 once it is ready.
> The v1 chatbot is still available [here](https://github.com/dborodin836/TF2-GPTChatBot/)

## Table Of Contents

- [Running Using Binary](#running-using-binary)
- [Running from Source](#running-from-source)
- [Usage](#usage)
    - [Basic Chat Commands](#basic-chat-commands)
        - [Quick-Query Commands](#quick-query-commands)
        - [Chat Commands](#chats)
        - [Clear Chat](#clear)
    - [Custom Models](#custom-language-models-oobabooga--text-generation-webui)
    - [That's all?](#thats-all)
    - [Screenshots](#screenshots)
    - [TF2 Bot Detector Cooperation](#tf2-bot-detector-cooperation-tf2bd)
- [Known Issues](#known-issues)
    - [Nickname Limitations](#nickname-limitations)

## Running Using Binary

### Prerequisites

- [OpenAI](https://platform.openai.com/account/api-keys) API key
- Steam and Team Fortress 2 installed on your machine

### 1. Download the latest nightly build from GitHub

You can download the latest nightly build [here](https://nightly.link/dborodin836/TF2-GPTChatBot/workflows/build/v2?preview).

### 2. Edit the configuration file:

Edit configuration.

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
- Node
- make
- [OpenAI](https://platform.openai.com/account/api-keys) API key
- Steam and Team Fortress 2 installed on your machine

You can you [Chocolatey](https://chocolatey.org/install) to install all the dependencies.
```sh
choco install make python310 nodejs-lts`
```
### 1. Installation

Clone the project repository:

```sh
git clone https://github.com/dborodin836/TF2-GPTChatBot.git
```

### 2. Navigate to the project directory:

```sh
cd TF2-GPTChatBot
```

### 3. Use make to run the project:

```sh
make dev
```

### 4. Add launch options to TF2 on Steam:

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
make build
```

## Usage

### Basic Chat Commands

Program comes with built-in chat commands. You can customize existent ones or add new ones to your liking.
This section only commands that are provided by **OpenAI**. This is because app was originally designed to support
OpenAI, but with time it has evolved to support any provider. But there are many other commands and providers
(**GroqCloud**, **TextGenerationWebUI**, etc.) available, and some of them are free to use. But they are not enabled by
default, and you need to enable them manually.

There are also thing so-called [prompts](https://github.com/dborodin836/TF2-GPTChatBot/wiki/Prompts) which allow you to 
customize how the model will response.

Check project [Wiki](https://github.com/dborodin836/TF2-GPTChatBot/wiki) for more info.

### Quick-query commands

These commands are used to generate a quick response from a language model.

Available commands: `!gpt3`, `!gpt4` and more!

### Usage examples

```
!gpt3 What is the meaning of life?
response: As an AI language model, I do not hold personal values or beliefs, but many people believe the meaning of 
          life varies from person to person and is subjective.
          
!gpt3 \demoman Hi!
response: Oy, laddie! Yer lookin' for some advice? Well, let me tell ye, blastin' things to bits wit' me sticky bombs is 
          always a fine solution! Just remember to always have a bottle of scrumpy on hand, and never trust a Spy.
```

### Chats

These commands are used to engage in conversations with the AI language model. In this community, chats are divided into
two main categories: **Global** and **Private**. 

- **Global Chats**: 🌍 These are accessible to all users on the server. It's the go-to spot for sharing thoughts, 
engaging in discussions, and having a good time together.

- **Private Chats**: 🤫 These are your personal zone where you can have uninterrupted conversations. Keep in mind, 
though, that even though it's private, others might still see it. 👀

Available commands: `!cgpt`(global), `!pc`(private) and more!

### !cgpt Usage examples

```
!cgpt Remember this number 42!
response: Okay, I will remember the number 42!

!cgpt What is the number?
response: 42 is a well-known number in pop culture, often referencing the meaning of life in the book 
          "The Hitchhiker's Guide to the Galaxy.
```

### !clear

Simply clears the chat history for specified command(s).

```
Command: !clear [\global] [\user='username'] [commands]

Description: Clears the chat history for specified command(s).

Calling without arguments clears own private chat history for any user.

Global Option (admin only):
  \global  Clears global chat history for specified command(s).
  
User Option (admin only):
  \user='username'  Clears private chat history for the specified user(s) for specified command(s).
  
Examples:
  For admin:
    !clear \global solly
    - Will clear global chat for solly command
    
    !clear \global \user='Pootis' \user='Soldier' solly
    - Will clear global and private chat for solly command for users with username "Pootis" and "Soldier"
    
  For everyone:
    !clear solly heavy
    - Will clear private chats for 'solly' and 'heavy' commands
```

## Custom language models (oobabooga / text-generation-webui)

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

## That's all?

**Of course not!** It's impossible to explain everything in one place. If you want to know more here are listed some things
that were left unexplained, and some tips and tricks: [unexplained_explained.md](docs/unexplained_explained.md) or at project [Wiki](https://github.com/dborodin836/TF2-GPTChatBot/wiki).

## Screenshots

[![image.png](https://ucarecdn.com/655e590a-1664-4424-8123-ae3a4e546ee3/)](https://ucarecdn.com/655e590a-1664-4424-8123-ae3a4e546ee3/)

## Known Issues

### Nickname Limitations

You cannot have a nickname that starts with a command name, such as !cgpt <your prompt>.

## TF2 Bot Detector Cooperation (TF2BD)

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
