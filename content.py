class Message:
    def __init__(self, message_type, value):
        self.message_type = message_type
        self.value = value


greetings = {
    "morning": Message("text", "Доброе утро, "),
    "night": Message("text", "Спокойной ночи, "),
    "hi": Message("text", "Привет, "),
    "welcome": Message("text", "Добро пожаловать, "),
    "happy_ny": Message("text", "С Новым Годом, ")
}