# Исполнитель бота

import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

bot = AsyncTeleBot('5451541586:AAG-_RxEiyoJdKHNQPAa6Gls5FCrZsrf_ks', 
                   state_storage=StateMemoryStorage())
bot.enable_saving_states()

def run():
    print('Привет! Добро пожаловать путник!\nДля отмены состояния напиши /cancel или нажми кнопку отмены\n\nДоступные команды презентации:\n/pages - ChoosePagesState выбор опции по страницам\n/options - ChooseOptionState выбор опции но без страниц (более лёгкий)\n/int - ChooseIntState ввод числа\n/str - ChooseStringState вводстроки\n/bool - ChooseConfirmState да / нет\n/del_12 - ChooseCustomState пример кастомного обработчика\n\n/css - ChooseStepState получение большого количества данных, с помощью малого количества кода')
    asyncio.run(bot.infinity_polling())