import json
import indicoio
from src.config import indicoio_api_key
from content import Message

indicoio.config.api_key = indicoio_api_key

messages = {}  # {sentiment_value: Message,...}

phrases_sentiment = json.load(open("data/sentiment/phrases.json"))
stickers_sentiment = json.load(open("data/sentiment/stickers.json"))

for k, v in phrases_sentiment.items():
    messages[v] = Message("text", k)

for k, v in stickers_sentiment.items():
    messages[v] = Message("sticker", k)

messages = dict(sorted(messages.items()))


def get_message(text):
    try:
        text_sentiment = indicoio.sentiment(text)
        print(text, text_sentiment)
        for k, v in messages.items():
            if k >= text_sentiment:
                return messages[k]
        return messages.values()[-1]
    except BaseException as e:
        print(e)
        return None
