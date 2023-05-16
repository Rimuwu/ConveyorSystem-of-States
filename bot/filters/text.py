# Фильтр текста, сюда можно добавить функцию локализации и определять сообщение по ключу

from bot.exec import bot
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.types import Message

class IsEqual(AdvancedCustomFilter):
    key = 'text'

    async def check(self, message: Message, key: str):
        return key == message.text

class StartWith(AdvancedCustomFilter):
    key = 'textstart'

    async def check(self, message: Message, key: str):
        return message.text.startswith(key)


bot.add_custom_filter(IsEqual())
bot.add_custom_filter(StartWith())