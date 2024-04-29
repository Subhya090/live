#!/usr/bin/python3
# coding: utf-8
# Developed by Tiago Neves
# Github: https://github.com/TiagoANeves
# Version: 1.0
# All rights reserved

# Import necessary modules
from telegram.ext import Updater, CommandHandler, MessageHandler
import telegram.ext.filters as filters
import requests
import re
import subprocess

# Get your UserName 
def whoami(update, context): 
    nome = update.message.chat.username
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=nome)

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

# Just an example to parse another URL and send the content.
def dog(update, context):
    chat_id = update.message.chat_id
    if update.message.chat.username == validuser:    
        url = get_image_url()
        context.bot.send_message(chat_id=chat_id, text="Segue a foto do catioro!")
        context.bot.send_photo(chat_id=chat_id, photo=url)
    else:
        context.bot.send_message(chat_id=chat_id, text="Usuário não permitido!")

# Runs any command on linux, Be careful
def opencmd(update, context):
    if update.message.chat.username == validuser:
        saida = subprocess.getoutput(update.message.text.lower())
        context.bot.send_message(chat_id=update.message.chat_id, text=saida)

# Runs any command on linux. Be careful
def cmd(update, context):
    chat_id = update.message.chat_id
    if update.message.chat.username == validuser:
       cmd_exec = ' '.join(context.args).lower()
       saida = subprocess.getoutput(cmd_exec)
       context.bot.send_message(chat_id=update.message.chat_id, text=saida)

# Check Disk, Memory and CPU Load
def check(update, context):
    chat_id = update.message.chat_id
    if update.message.chat.username == validuser:
        cmd_exec = ' '.join(context.args).lower()
        if cmd_exec == 'disk':
            saida = subprocess.getoutput('df -h')
            context.bot.send_message(chat_id=update.message.chat_id, text=saida)
        elif cmd_exec == 'memory':
            saida = subprocess.getoutput('free -m')
            context.bot.send_message(chat_id=update.message.chat_id, text=saida)
        elif cmd_exec == 'cpu':
            saida = subprocess.getoutput('uptime')
            context.bot.send_message(chat_id=update.message.chat_id, text=saida)

# Send the available commands.
def helpme(update, context):
    chat_id = update.message.chat_id
    if update.message.chat.username == validuser:
        context.bot.send_message(chat_id=update.message.chat_id, text="Comandos Configuados: \
                                        \n/help \
                                        \n/dog \
                                        \n/cmd <comando> Só use se souber o que está fazendo! \
                                        \n/check (disk, memory, cpu)")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Comandos Configuados: \n/help\n/dog")

# Main - Define the Handler.
def main():
    global validuser 
    # Valid user to run commands.
    validuser = 'iamsamir090'
    # Bot token
    updater = Updater('6572573718:AAHRAkfghAKDhR0nWxNR9uQxQrds680JLMc', use_context=True)
    dp = updater.dispatcher
    # Command Handlers
    dp.add_handler(CommandHandler('dog', dog))
    dp.add_handler(CommandHandler('whoami', whoami))
    dp.add_handler(CommandHandler('help', helpme))
    dp.add_handler(CommandHandler('start', helpme))
    dp.add_handler(CommandHandler('cmd', cmd, pass_args=True))
    dp.add_handler(CommandHandler('check', check, pass_args=True))
    # Message Handler, you can run any commands on a Linux machine. Be careful
    dp.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, opencmd))
    updater.start_polling()
    updater.idle()

# Main
if __name__ == '__main__':
    main()
