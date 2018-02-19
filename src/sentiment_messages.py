import json
import indicoio
from src.config import indicoio_api_key
from content import Message
import random
import time
import src.translator as translator

random.seed(int(time.time()))

language_proportions = []


def set_language_proportions():
    global language_proportions
    language_proportions = [
        random.random(),  # original messages
        random.random()  # English messages
    ]

    print(language_proportions)


indicoio.config.api_key = indicoio_api_key

messages = {}  # {sentiment_value: Message,...}

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


def get_message(text):
    try:
        text_sentiment = \
            indicoio.sentiment(random.choices([text, translator.translate(text)], weights=language_proportions)[0])
        print(text_sentiment)
        sentiments = sorted(list(messages.keys()))
        result_sentiment = None
        for i, s in enumerate(sentiments):
            if s > text_sentiment:
                if s == sentiments[-1] or abs(s - text_sentiment) < abs(sentiments[i - 1] - text_sentiment):
                    result_sentiment = s
                    break
                else:
                    result_sentiment = sentiments[i-1]
                    break
        if result_sentiment is None:
            result_sentiment = sentiments[-1]
        return random.choice(messages[result_sentiment])
    except BaseException as e:
        print(e)
    return None
