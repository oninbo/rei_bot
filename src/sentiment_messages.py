import json
import indicoio
from src.config import indicoio_api_key
from content import Message
import random
import time
import src.translator as translator
from src.logger import logger
import emoji, re

random.seed(int(time.time()))

language_proportions = []

mood_value = 0.5


def set_language_proportions():
    global language_proportions
    language_proportions = [
        random.random(),  # original messages
        random.random()  # English messages
    ]

    logger.info(["language proportions", language_proportions])


def set_mood(value=None):
    global mood_value
    if value is None:
        mood_value = random.random()
    else:
        mood_value = value

    logger.info(['mood', mood_value])


indicoio.config.api_key = indicoio_api_key

messages = {} # {sentiment_value: Message,...}

emoji_sentiment = json.load(open("data/sentiment/emoji.json"))

# TODO: use text messages only in case of keyword search
"""
phrases_sentiment = json.load(open("data/sentiment/phrases.json")) 

for s, v in phrases_sentiment.items():
    if v not in messages:
        messages[v] = []
    messages[v].append(Message("text", s))
"""

stickers_path = "data/sentiment/stickers.json"

stickers_sentiment = json.load(open(stickers_path))

for s, v in stickers_sentiment.items():
    if v not in messages.keys():
        messages[v] = []
    messages[v].append(Message("sticker", s))


sentiments = sorted(list(messages.keys()))


def update_messages():
    global stickers_sentiment, messages, sentiments

    stickers_sentiment = json.load(open(stickers_path))

    messages = {}

    for s, v in stickers_sentiment.items():
        if v not in messages.keys():
            messages[v] = []
        messages[v].append(Message("sticker", s))

    sentiments = sorted(list(messages.keys()))


def get_message(text):
    global mood_value
    try:
        if len(text) > 0:
            text_sentiment = sentiment_from_text(text)
            total_sentiment = (6 * text_sentiment + 4 * mood_value) / 10
            logger.debug(['total sentiment', total_sentiment])
            result_sentiment = chose_message(total_sentiment)
            set_mood((2 * text_sentiment + 8 * mood_value) / 10)
        else:
            result_sentiment = chose_message(mood_value)
    except Exception as e:
        logger.exception(e)
        return None
    if len(messages) > 0:
        return random.choice(messages[result_sentiment])
    else:
        return None


def sentiment_from_text(text):
    emojis = re.findall(emoji.get_emoji_regexp(), text)
    text_sentiment = 0
    for e in emojis:
        if e in emoji_sentiment.keys():
            text_sentiment += emoji_sentiment[e]
    is_original = random.choices([True, False], weights=language_proportions)[0]
    if not is_original:
        text = translator.translate(text)
    text_sentiment += indicoio.sentiment(text)
    text_sentiment /= len(emojis)+1
    logger.debug([text, text_sentiment])

    return text_sentiment


def chose_message(sentiment):
    global sentiments
    result_sentiment = None
    for i, s in enumerate(sentiments):
        if s > sentiment:
            if s == sentiments[-1] or abs(s - sentiment) < abs(sentiments[i - 1] - sentiment):
                result_sentiment = s
                break
            else:
                result_sentiment = sentiments[i - 1]
                break
    if result_sentiment is None and len(sentiments) > 0:
        result_sentiment = sentiments[-1]
    return result_sentiment


def add_stickers_sentiment(stickers):
    global stickers_sentiment
    for sticker in stickers:
        if sticker.file_id not in stickers_sentiment and sticker.emoji in emoji_sentiment:
            stickers_sentiment[sticker.file_id] = emoji_sentiment[sticker.emoji]
    with open(stickers_path, 'w') as f:
        f.write(json.dumps(stickers_sentiment, indent=4))
    f.closed
    update_messages()


def delete_stickers(stickers):
    global stickers_sentiment
    for sticker in stickers:
        if sticker.file_id in stickers_sentiment:
            del stickers_sentiment[sticker.file_id]
    with open(stickers_path, 'w') as f:
        f.write(json.dumps(stickers_sentiment, indent=4))
    f.closed
    update_messages()
