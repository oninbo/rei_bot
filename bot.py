import telebot
import config
import content
import random

bot = telebot.TeleBot(config.token)

on = True


@bot.message_handler(commands=['start'])
def set_on(message):
    global on
    on = True


@bot.message_handler(commands=['stop'])
def set_on(message):
    global on
    on = False


@bot.message_handler(func=lambda message: True, content_types=['text'])
def reply(message):
    print(message.message_id)
    global on
    if on and to_say():
        say(message)


def to_say():
    r = random.randint(1, 1000)
    if r <= 200:
        return True
    else:
        return False


def say(message):
        print(bot.send_message(message.chat.id, content.messages[random.randint(0, len(content.messages)-1)].value).message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)