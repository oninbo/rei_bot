import time
import telebot
import config
import content
import random
import math
import copy

bot = telebot.TeleBot(config.token)

messages_handled = {}
messages_range = 100
max_probability = 0.2
phrases = []


def fill_phrases():
    phrases = copy.deepcopy(content.messages)
    random.shuffle(phrases)


@bot.message_handler(commands=['start'])
def start_message(message):
    #print(message)
    say(message)


@bot.message_handler(commands=['ask'])
def ping(message):
    #print(message)
    reply(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker', 'photo'])
def send_message(message):
    chat_id = message.chat.id
    #global messages_handled
    if chat_id not in messages_handled:
        messages_handled[chat_id] = 0
    else:
        messages_handled[chat_id] += 1
    if message.chat.type == 'private' and to_say(0.5, chat_id):
        say(message)
    elif check_reply(message):
        reply(message)
    if to_say(math.cos(messages_handled[chat_id])*max_probability, chat_id):
        say(message)


def check_reply(message):
    if message.reply_to_message and message.reply_to_message.from_user.username == bot.get_me().username:
        return True


def to_say(probability, chat_id):
    #print(probability)
    '''global messages_handled, messages_range
    if messages_handled[chat_id] > messages_range:
        random.seed(int(time.time()))
        messages_handled[chat_id] = 0'''
    if phrases:
        fill_phrases()
    max = 10000
    r = random.randint(1, max+1)
    #print(r)
    if r <= max*probability:
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
    #return content.messages[random.randint(0, len(content.messages)-1)].value
    return content.messages.pop().value


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except BaseException:
            time.sleep(10)