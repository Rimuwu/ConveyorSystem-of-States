# Исполнитель бота

import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

bot = AsyncTeleBot('TOKEN', 
                   state_storage=StateMemoryStorage())
bot.enable_saving_states()

def run():
    print('start')
    asyncio.run(bot.infinity_polling())