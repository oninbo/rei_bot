from src.config import google_ai_token
import apiai, json
from content import Message

CLIENT_ACCESS_TOKEN = google_ai_token

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)


def get_message(text):
    request = ai.text_request()
    request.query = text

    request.lang = 'ru'

    response = json.loads(request.getresponse().read())
    result_text = response['result']['fulfillment']['speech']

    if result_text and result_text != 'None':
        return Message('text', result_text)
    else:
        return None
