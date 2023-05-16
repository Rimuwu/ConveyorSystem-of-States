from bot.exec import bot
from bot.modules.tools import ChooseOptionState
from bot.modules.markup import list_to_keyboard
from telebot.types import ReplyKeyboardRemove

names = {'Артемий': 1, 'Андрей': 2, "Иван": 3, 
         "Тимофей": 4, "Вика": 5, "Саша": 6, "Фёдор": 7, "Юрий": 8}

async def adp(res, transmitted_data: dict):
    """ Функция обработки выбранного элемента
    """
    userid = transmitted_data['userid']
    await bot.send_message(userid, f'По моим данным этот человек под номером {res}', reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['options'])
async def test_options(message):
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code
    
    markup = list_to_keyboard([list(names.keys()), ["❌ Отмена"]])
    await bot.send_message(userid, f'Выберите имя', reply_markup=markup)
    
    await ChooseOptionState(
        adp, userid, chatid, lang, names)