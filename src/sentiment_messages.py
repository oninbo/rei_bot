import json
import indicoio
from src.config import indicoio_api_key
from content import Message
import random
import time
import src.translator as translator
from src.logger import logger

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

# TODO: use text messages only in case of keyword search
"""
phrases_sentiment = json.load(open("data/sentiment/phrases.json")) 

for s, v in phrases_sentiment.items():
    if v not in messages:
        messages[v] = []
    messages[v].append(Message("text", s))
"""

stickers_sentiment = json.load(open("data/sentiment/stickers.json"))

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
    return random.choice(messages[result_sentiment])


def sentiment_from_text(text):
    is_original = random.choices([True, False], weights=language_proportions)[0]
    if not is_original:
        text = translator.translate(text)
    text_sentiment = indicoio.sentiment(text)
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
    if result_sentiment is None:
        result_sentiment = sentiments[-1]
    return result_sentiment
