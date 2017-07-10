import time
import telebot
import config
import content
import random

bot = telebot.TeleBot(config.token)

messages_handled = {}
messages_range = 10


@bot.message_handler(commands=['start'])
def ping(message):
    #print(message)
    say(message)


@bot.message_handler(commands=['ask'])
def ping(message):
    #print(message)
    reply(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker', 'photo'])
def send_message(message):
    chat_id = message.chat.id
    global messages_handled
    if chat_id not in messages_handled:
        messages_handled[chat_id] = 0
    else:
        messages_handled[chat_id] += 1
    print(message.chat)
    if message.chat.type == 'private':
        say(message)
    elif check_reply(message):
        reply(message)
    if to_say(messages_handled[chat_id]/100*2, chat_id):
        say(message)


def check_reply(message):
    if message.reply_to_message and message.reply_to_message.from_user.username == 'Rei_Ayanami_2017_bot':
        return True


def to_say(probability, chat_id):
    global messages_handled, messages_range
    if messages_handled[chat_id] > messages_range:
        messages_handled[chat_id] = 0
        random.seed(int(time.time()))
    r = random.randint(1, 1000)
    if r <= 1000*probability:
        #print("yes")
        return True


def say(message):
    bot.send_message(message.chat.id, get_phrase())


def reply(message, text=None):
    if text:
        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, get_phrase(), reply_to_message_id=message.message_id)


def get_phrase():
    return content.messages[random.randint(0, len(content.messages)-1)].value




if __name__ == '__main__':
    bot.polling(none_stop=True)