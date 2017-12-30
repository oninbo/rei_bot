import time
import telebot
import config
import content
import random
import copy
import db_manager

bot = telebot.TeleBot(config.token)

messages_handled = {}
messages_range = 100
max_probability = 0.01
phrases = []


def fill_phrases():
    global phrases
    phrases = content.messages + db_manager.get_quote_db_list()
    random.shuffle(phrases)


@bot.message_handler(commands=['add_sticker'])
def add_sticker(message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message
    if reply_message and reply_message.content_type == 'sticker':
        sticker = content.Message("sticker", reply_message.sticker.file_id)
        db_manager.add_to_quote_db(sticker)
        fill_phrases()
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
        fill_phrases()
        bot.send_message(chat_id, "The sticker has been successfully deleted")
    else:
        bot.send_message(chat_id, "Error. Wrong message type")


@bot.message_handler(commands=['say_all'])
def say_all(message):
    if not phrases:
        fill_phrases()
    for i in range(0, len(phrases)):
        say(message)


@bot.message_handler(commands=['start'])
def start_message(message):
    say(message)


def get_greeting(name, key):
    greeting = copy.deepcopy(content.greetings[key])
    if name in content.names:
        name = content.names[name]
    greeting.value += name
    return greeting


@bot.message_handler(commands=['ask'])
def ping(message):
    print(message.reply_to_message)
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


@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker', 'photo'])
def reply_default_message(message):
    print(message)
    chat_id = message.chat.id
    if chat_id not in messages_handled:
        messages_handled[chat_id] = 0
    else:
        messages_handled[chat_id] += 1
    if message.chat.type == 'private' and to_say(0.5, chat_id):
        say(message)
    elif check_reply(message):
        reply(message)
    if to_say(max_probability, chat_id):
        say(message)


@bot.message_handler(func=lambda message: True, content_types=['new_chat_members'])
def say_welcome(message):
    print(message)
    greeting = get_greeting(message.new_chat_member.first_name, 'welcome')
    say(message, greeting)


def check_reply(message):
    if message.reply_to_message and message.reply_to_message.from_user.username == bot.get_me().username:
        return True


def to_say(probability, chat_id):
    #print(probability)
    '''global messages_handled, messages_range
    if messages_handled[chat_id] > messages_range:
        messages_handled[chat_id] = 0'''
    max = 10000
    r = random.randint(1, max+1)
    #print(r)
    if r <= max*probability:
        #print("yes")
        return True


send_functions = {}
send_functions["sticker"] = bot.send_sticker
send_functions["text"] = bot.send_message
send_functions["video"] = bot.send_video
send_functions["photo"] = bot.send_photo


def say(message, message_to_say=None):
    if message_to_say == None:
        message_to_say = get_message()
    send_functions[message_to_say.message_type](message.chat.id, message_to_say.value)


def reply(message, text=None):
    if text:
        send_functions[message.message_type](message.chat.id, text, reply_to_message_id=message.message_id)
    else:
        message_to_say = get_message()
        print(message_to_say.message_type)
        send_functions[message_to_say.message_type](message.chat.id, message_to_say.value, reply_to_message_id=message.message_id)


def get_message():
    if not phrases:
        n = int(time.time())
        random.seed(n)
        fill_phrases()
    #return content.messages[random.randint(0, len(content.messages)-1)].value
    return phrases.pop()


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except BaseException:
            time.sleep(10)