import configparser
import os
import sys
from os.path import exists

CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

if not exists(CONFIG_FILE):
    print("Couldn't find 'config.ini' file.")
    os.system('pause')
    sys.exit(1)

TF2_LOGFILE_PATH = config['GENERAL']['TF2_LOGFILE_PATH']
OPENAI_API_KEY = config['GENERAL']['OPENAI_API_KEY']

GPT_COMMAND = config['COMMANDS']['GPT_COMMAND']
CHATGPT_COMMAND = config['COMMANDS']['CHATGPT_COMMAND']
CLEAR_CHAT_COMMAND = config['COMMANDS']['CLEAR_CHAT_COMMAND']

RCON_HOST = config['RCON']['RCON_HOST']
RCON_PASSWORD = config['RCON']['RCON_PASSWORD']
RCON_PORT = int(config['RCON']['RCON_PORT'])

SOFT_COMPLETION_LIMIT = config['MISC']['SOFT_COMPLETION_LIMIT']
HARD_COMPLETION_LIMIT = int(config['MISC']['HARD_COMPLETION_LIMIT'])
