from bot.exec import bot
from bot.modules.tools import ChooseCustomState
from telebot.types import Message


async def custom_hendler(messga: Message, transmitted_data):
    """ В момент проверки вызывается эта функция и она определяет, правильно ли пользователь ввёл данные
    """
    userid = transmitted_data['userid']
    content = str(messga.text)

    if content.isdigit() and int(content) // 12 != 0:
        return True, int(content)
    else:
        await bot.send_message(userid, f'Введённые данные не делятся на 12')
        return False, None

async def adp(unit: int, transmitted_data: dict):
    """ Функция обработки выбранного элемента
    """
    userid = transmitted_data['userid']
    await bot.send_message(userid, f'Ответ деления на 12 - {unit // 12}')

@bot.message_handler(commands=['del_12'])
async def test_custom(message):
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code
    
    await bot.send_message(userid, f'Введитее число, которое делится на 12')
    
    await ChooseCustomState(
        adp, custom_hendler, userid, chatid, lang
        )