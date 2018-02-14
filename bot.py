import time
import telebot
import config
import content
import random
import copy
import db_manager
from logger import logger, fh
from logging import INFO

telebot.logger.addHandler(fh)
telebot.logger.setLevel(INFO)

bot = telebot.TeleBot(config.token)


messages_handled = {}
messages_range = 100
max_probability = 0.01
chat_phrases = {}


def fill_phrases():
    random.seed(int(time.time()))
    phrases = content.messages + db_manager.get_quote_db_list()
    random.shuffle(phrases)
    return phrases


def update_phrases():
    global chat_phrases
    for p in chat_phrases:
        p = fill_phrases()


@bot.message_handler(commands=['add_sticker'])
def add_sticker(message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message
    if reply_message and reply_message.content_type == 'sticker':
        sticker = content.Message("sticker", reply_message.sticker.file_id)
        db_manager.add_to_quote_db(sticker)
        update_phrases()
        bot.send_message(chat_id, "The sticker has been successfully added")
    else:
        bot.send_message(chat_id, "Error. Wrong message type")


@bot.message_handler(commands=['delete_sticker'])
def delete_sticker(message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message
    if reply_message and reply_message.content_type == 'sticker':
        sticker = content.Message("sticker", reply_message.sticker.file_id)
        db_manager.remove_from_quote_db(sticker)
        update_phrases()
        bot.send_message(chat_id, "The sticker has been successfully deleted")
    else:
        bot.send_message(chat_id, "Error. Wrong message type")


@bot.message_handler(commands=['say_all'])
def say_all(message):
    phrases = fill_phrases()
    for i, p in enumerate(phrases):
        send_functions[p.message_type](message.chat.id, p.value)
    send_functions["text"](message.chat.id, "Done")


@bot.message_handler(commands=['logs'])
def say_all(message):
    bot.send_document(config.creator_id, open("logs/logs"))


@bot.message_handler(commands=['start'])
def start_message(message):
    say(message)


def get_greeting(name, key):
    greeting = copy.deepcopy(content.greetings[key])
    greeting.value += name
    return greeting


@bot.message_handler(commands=['ask'])
def ping(message):
    reply(message)


@bot.message_handler(commands=['night'])
def say_good_night(message):
    say(message, get_greeting(message.from_user.first_name, 'night'))


@bot.message_handler(commands=['morning'])
def say_good_morning(message):
    say(message, get_greeting(message.from_user.first_name, 'morning'))


@bot.message_handler(commands=['hi'])
def say_good_morning(message):
    say(message, get_greeting(message.from_user.first_name, 'hi'))


@bot.message_handler(commands=['happy_ny'])
def say_good_morning(message):
    say(message, get_greeting(message.from_user.first_name, 'happy_ny'))


@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker', 'photo'])
def reply_default_message(message):
    chat_id = message.chat.id
    if message.chat.type == 'private' and to_say(0.5):
        say(message)
    elif check_reply(message):
        reply(message)
    if to_say(max_probability):
        say(message)


@bot.message_handler(func=lambda message: True, content_types=['new_chat_members'])
def say_welcome(message):
    logger.debug(message)
    greeting = get_greeting(message.new_chat_member.first_name, 'welcome')
    say(message, greeting)


def check_reply(message):
    if message.reply_to_message and message.reply_to_message.from_user.username == bot.get_me().username:
        return True


def to_say(probability):
    _max = 10000
    r = random.randint(1, _max+1)
    if r <= _max*probability:
        return True


send_functions = {}
send_functions["sticker"] = bot.send_sticker
send_functions["text"] = bot.send_message
send_functions["video"] = bot.send_video
send_functions["photo"] = bot.send_photo


def say(message, message_to_say=None):
    logger.info(message)
    if message_to_say == None:
        message_to_say = get_message(message.chat.id)
    send_functions[message_to_say.message_type](message.chat.id, message_to_say.value)


def reply(message, text=None):
    logger.info(message)
    if text:
        send_functions[message.message_type](message.chat.id, text, reply_to_message_id=message.message_id)
    else:
        message_to_say = get_message(message.chat.id)
        send_functions[message_to_say.message_type](message.chat.id, message_to_say.value, reply_to_message_id=message.message_id)


def get_message(chat_id):
    if chat_id not in chat_phrases:
        chat_phrases[chat_id] = []
    if len(chat_phrases[chat_id]) == 0:
        chat_phrases[chat_id] = fill_phrases()
    message = chat_phrases[chat_id].pop()
    return message


def death_notify():
    bot.send_message(config.creator_id, "Looks like I'm dead now")


def alive_notify():
    bot.send_message(config.creator_id, "Looks like I'm alive now")


if __name__ == '__main__':
    while True:
        logger.debug('trying to connect')
        try:
            alive_notify()
            bot.polling(none_stop=True)
        except BaseException as e:
            logger.info("Some shit happened")
            logger.error(e)
            try:
                death_notify()
            except:
                pass
        logger.debug('wait for 10 seconds')
        time.sleep(10)
