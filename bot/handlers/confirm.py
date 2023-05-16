from bot.exec import bot
from bot.modules.tools import ChooseConfirmState
from bot.modules.markup import list_to_keyboard
from telebot.types import ReplyKeyboardRemove

async def adp(result: bool, transmitted_data: dict):
    """ Функция обработки выбранного элемента
    """
    userid = transmitted_data['userid']
    await bot.send_message(userid, f'Вы выбрали {result}', reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['bool'])
async def test_confirm(message):
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code
    
    # При отрецательном ответе и cancel = True вызывает states/cancel()
    cancel = False
    
    markup = list_to_keyboard([["✅ Включить", "❌ Выключить"]])
    await bot.send_message(userid, f'Включить прослушку?', reply_markup=markup)
    
    await ChooseConfirmState(
        adp, userid, chatid, lang, cancel
        )