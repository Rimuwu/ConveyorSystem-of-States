#Активация встроенных фильтров
from bot.exec import bot
from telebot.asyncio_filters import IsDigitFilter, StateFilter

bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(IsDigitFilter())