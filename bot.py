import telebot
from src import config
from src.logger import fh, log_file
from logging import INFO
from src.messages_methods import *
import src.google_ai as ai

telebot.logger.addHandler(fh)
telebot.logger.setLevel(INFO)

bot = telebot.TeleBot(config.bot_token)

polling_interval = 15


@bot.message_handler(commands=['add_sticker'])
def add_sticker_handler(message):
    reply_message = message.reply_to_message
    if reply_message and reply_message.content_type == 'sticker':
        add_stickers([reply_message.sticker])
        bot.reply_to(message, "The sticker has been successfully added")
    else:
        bot.reply_to(message, "Error. Wrong message type")


@bot.message_handler(commands=['delete_sticker'])
def delete_sticker_handler(message):
    reply_message = message.reply_to_message
    if reply_message and reply_message.content_type == 'sticker':
        delete_stickers([reply_message.sticker])
        bot.reply_to(message, "The sticker has been successfully deleted")
    else:
        bot.reply_to(message, "Error. Wrong message type")


@bot.message_handler(commands=['add_sticker_set'])
def add_sticker_set(message):
    reply_message = message.reply_to_message
    if reply_message and reply_message.content_type == 'sticker':
        sticker_set = bot.get_sticker_set(reply_message.sticker.set_name)
        add_stickers(sticker_set.stickers)
        bot.reply_to(message, "The sticker pack has been successfully added")
    else:
        bot.reply_to(message, "Error. Wrong message type")


@bot.message_handler(commands=['delete_sticker_set'])
def add_sticker_set(message):
    reply_message = message.reply_to_message
    if reply_message and reply_message.content_type == 'sticker':
        sticker_set = bot.get_sticker_set(reply_message.sticker.set_name)
        delete_stickers(sticker_set.stickers)
        bot.reply_to(message, "The sticker pack has been successfully removed")
    else:
        bot.reply_to(message, "Error. Wrong message type")


@bot.message_handler(commands=['say_all'])
def say_all(message):
    phrases = fill_phrases()
    for i, p in enumerate(phrases):
        send_functions[p.message_type](bot, message.chat.id, p.value)
    send_functions["text"](bot, message.chat.id, "Done")


@bot.message_handler(commands=['logs'])
def say_all(message):
    bot.send_document(config.creator_id, open(log_file))


@bot.message_handler(commands=['debug'])
def set_debug(message):
    global debug_mode
    debug_mode = not debug_mode
    notification = "Debug mode is"
    if debug_mode:
        notification += " on"
    else:
        notification += " off"
    logger.debug('debug mode ' + str(debug_mode))
    bot.send_message(config.creator_id, notification)


@bot.message_handler(commands=['ask'])
def ping(message):
    if message.chat.type == 'private' or check_mention(bot.get_me().username, message):
        if message.reply_to_message:
            reply(bot, message.reply_to_message)
        else:
            reply(bot, message)


@bot.message_handler(commands=['night'])
def say_good_night(message):
    reply(bot, message, get_greeting(message.from_user.first_name, 'night'))


@bot.message_handler(commands=['morning'])
def say_good_morning(message):
    reply(bot, message, get_greeting(message.from_user.first_name, 'morning'))


@bot.message_handler(commands=['hi'])
def say_good_morning(message):
    reply(bot, message, get_greeting(message.from_user.first_name, 'hi'))


@bot.message_handler(commands=['happy_ny'])
def say_good_morning(message):
    reply(bot, message, get_greeting(message.from_user.first_name, 'happy_ny'))


@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker'])
def reply_message(message):
    if message.content_type == 'text':
        ai_message = ai.get_message(message.text)
        if ai_message:
            reply(bot, message, message_to_say=ai_message)
    if check_mention(bot.get_me().username, message) or check_reply(bot.get_me().username, message):
        reply(bot, message)
    elif message.chat.type == 'private':
        if (debug_mode and message.chat.id == config.creator_id) or message.content_type == 'text' and check_question(message.text):
            reply(bot, message)
    elif to_say():
        reply(bot, message)


@bot.message_handler(func=lambda message: True, content_types=['new_chat_members'])
def say_welcome(message):
    logger.debug(message)
    greeting = get_greeting(message.new_chat_member.first_name, 'welcome')
    say(bot, message, greeting)


def death_notify():
    bot.send_message(config.creator_id, "Looks like I'm dead now")


def alive_notify():
    bot.send_message(config.creator_id, "Looks like I'm alive now")


def launch():
    wait_time = 10
    error_interval = 100
    error_time = None
    while True:
        logger.debug('trying to connect')
        try:
            alive_notify()
            sentiment_messages.set_language_proportions()
            set_probability(sentiment_messages.mood_value)
            bot.polling(none_stop=True, interval=polling_interval)
        except BaseException as e:
            logger.exception(e)
            if error_time:
                if time.time() - error_time < error_interval:
                    wait_time = wait_time*2
                else:
                    wait_time = wait_time/2
            error_time = time.time()

            try:
                death_notify()
            except:
                pass
        logger.debug('wait for '+ str(wait_time) + ' seconds')
        time.sleep(wait_time)


if __name__ == '__main__':
    launch()
