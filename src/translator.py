from yandex_translate import YandexTranslate
from src.config import yandex_api_key

ya_translator = YandexTranslate(yandex_api_key)


def translate(text):
    return ya_translator.translate(text, 'ru-en')['text'][0]
