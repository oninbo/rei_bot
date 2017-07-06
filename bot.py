import telebot
import config
import content
import random

bot = telebot.TeleBot(config.token)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_message(message):
    print(message.reply_to_message)
    if check_reply(message):
        reply(message)
    elif to_say():
        say(message)



def check_reply(message):
    if message.reply_to_message and message.reply_to_message.from_user.username == 'Rei_Ayanami_2017_bot':
        return True


def to_say():
    r = random.randint(1, 1000)
    if r <= 200:
        return True


def say(message):
    bot.send_message(message.chat.id, content.messages[random.randint(0, len(content.messages)-1)].value)


def reply(message):
    bot.send_message(message.chat.id, content.messages[random.randint(0, len(content.messages) - 1)].value, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)