import telebot
import config
import content
import random

bot = telebot.TeleBot(config.token)

messages_handled = 0
messages_range = 10


@bot.message_handler(commands=['alive'])
def ping(message):
    reply(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker', 'photo'])
def send_message(message):
    global messages_handled
    messages_handled += 1
    #print(message.text)
    if check_reply(message):
        reply(message)
    elif to_say():
        say(message)


def check_reply(message):
    if message.reply_to_message and message.reply_to_message.from_user.username == 'Rei_Ayanami_2017_bot':
        return True


def to_say():
    global messages_handled, messages_range
    if messages_handled >= messages_range:
        messages_handled = 0
        r = random.randint(1, 1000)
        if r <= 200:
            #print("yes")
            return True


def say(message):
    bot.send_message(message.chat.id, get_phrase())


def reply(message):
    bot.send_message(message.chat.id, get_phrase(), reply_to_message_id=message.message_id)


def get_phrase():
    return content.messages[random.randint(0, len(content.messages)-1)].value




if __name__ == '__main__':
    bot.polling(none_stop=True)