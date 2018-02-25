from src import db_manager, sentiment_messages
import random, time, re, content, copy
from src.logger import logger
from telebot import TeleBot

debug_mode = False

phrases = db_manager.get_quote_db_list()
say_probability = 0.5
chat_phrases = {}


def fill_phrases():
    global phrases
    random.seed(int(time.time()))
    _phrases = copy.copy(phrases)
    random.shuffle(_phrases)
    return _phrases


def update_phrases():
    global phrases
    phrases = db_manager.get_quote_db_list()
    global chat_phrases
    for p in chat_phrases:
        p = fill_phrases()


def add_stickers(stickers):
    for sticker in stickers:
        db_manager.add_to_quote_db(content.Message("sticker", sticker.file_id))
    sentiment_messages.add_stickers_sentiment(stickers)
    update_phrases()


def delete_stickers(stickers):
    for sticker in stickers:
        db_manager.remove_from_quote_db(content.Message("sticker", sticker.file_id))
    sentiment_messages.delete_stickers(stickers)
    update_phrases()


def check_reply(username, message):
    return message.reply_to_message and message.reply_to_message.from_user.username == username


def check_mention(username, message):
    if message.content_type == 'text' and message.entities:
        for e in message.entities:
            mention_text = message.text[e.offset:e.offset+e.length]
            return len(re.findall(username, mention_text)) > 0
    return False


def remove_commands(text):
    commands = re.findall("\/[a-zA-Z0-9_]+", text)
    for c in commands:
        text = text.replace(c, "")
    return text


def remove_mentions(text):
    mentions = re.findall("@[a-zA-Z0-9_]+", text)
    for m in mentions:
        text = text.replace(m, "")
    return text


def check_question(text):
    return len(re.findall("\\?", text)) > 0


send_functions = {}
send_functions["sticker"] = TeleBot.send_sticker
send_functions["text"] = TeleBot.send_message
send_functions["video"] = TeleBot.send_video
send_functions["photo"] = TeleBot.send_photo


def say(bot, message, message_to_say=None, reply=None):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(3)
    logger.info(message)
    if not message_to_say:
        message_to_say = get_message(message)
    if message_to_say:
        send_functions[message_to_say.message_type](bot, message.chat.id, message_to_say.value, reply_to_message_id=reply)


def reply(bot, message, message_to_say=None):
    say(bot, message, message_to_say=message_to_say, reply=message.message_id)


def set_probability(value):
    global say_probability
    say_probability = value/10


def get_message(message):
    if message.content_type == 'text':
        sentiment_message = sentiment_messages.get_message(remove_mentions(remove_commands(message.text)))
    elif message.content_type == 'sticker':
        sentiment_message = sentiment_messages.get_message(message.sticker.emoji)
    if sentiment_message is not None:
            logger.info('sentimental')
            set_probability(sentiment_messages.mood_value)
            return sentiment_message
    chat_id = message.chat.id
    if chat_id not in chat_phrases:
        chat_phrases[chat_id] = []
    if len(chat_phrases[chat_id]) == 0:
        chat_phrases[chat_id] = fill_phrases()
    if len(chat_phrases[chat_id]) > 0:
        message = chat_phrases[chat_id].pop()
    else:
        return None
    return message


def to_say():
    return random.choices([True, False], weights=[say_probability, 1 - say_probability])[0]


def get_greeting(name, key):
    greeting = copy.deepcopy(content.greetings[key])
    greeting.value += name
    return greeting