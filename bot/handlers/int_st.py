from bot.exec import bot
from bot.modules.tools import ChooseIntState
from bot.modules.markup import list_to_keyboard
from telebot.types import ReplyKeyboardRemove

async def adp(unit: int, transmitted_data: dict):
    """ Функция обработки выбранного числа
    """
    userid = transmitted_data['userid']
    await bot.send_message(userid, f'Вы ввели {unit}', reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['int'])
async def test_int(message):
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code
    
    min_int = 12
    max_int = 100
    
    markup = list_to_keyboard(["❌ Отмена"])
    await bot.send_message(userid, f'Выберите число от {min_int} до {max_int}', reply_markup=markup)
    
    await ChooseIntState(
        adp, userid, chatid, lang, 
        min_int=min_int, max_int=max_int
        )