from bot.exec import bot
from bot.modules.tools import ChooseStringState
from bot.modules.markup import list_to_keyboard
from telebot.types import ReplyKeyboardRemove

async def adp(string: str, transmitted_data: dict):
    """ Функция обработки введённой строки
    """
    userid = transmitted_data['userid']
    await bot.send_message(userid, f'Вы ввели {string}', reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['str'])
async def test_str(message):
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code
    
    min_len = 2
    max_len = 100
    
    markup = list_to_keyboard(["❌ Отмена"])
    await bot.send_message(userid, f'Введите сообщение длинной от {min_len} до {max_len}', reply_markup=markup)
    
    await ChooseStringState(
        adp, userid, chatid, lang, 
        min_len=min_len, max_len=max_len
        )