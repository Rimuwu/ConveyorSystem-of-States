from bot.exec import bot
from bot.modules.tools import ChoosePagesState, ChooseStepState
from random import choice

names = ['Артемий', 'Андрей', "Иван", 
         "Тимофей", "Вика", "Саша", "Фёдор", "Юрий"]
general_dict = {
    "➕ Добавить": 'add',
    "🕳 Очистить": 'reset'
}

async def adp(res, transmitted_data):
    """ Функция обработки выбранного элемента
    """
    key = transmitted_data['key']
    options = transmitted_data['options']
    userid = transmitted_data['userid']

    await bot.send_message(userid, f'Ты выбрал {key}, по моим данным эта кнопка отвечает за {res}')

    if res == 'add':
        r_name = choice(names)
        if r_name in options:
            r_name = r_name + str(list(options.keys()).count(r_name)+1)
        add = {r_name: 'user'}
        return {'status': 'edit', 'elements': {'add': add}}
    
    elif res == 'user':
        return {'status': 'edit', 'elements': {'delete': [key]}}
    
    elif res == 'reset':
        return {'status': 'update', 'options': general_dict}
    
@bot.message_handler(commands=['pages'])
async def test_options_pages(message):
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code
    
    await ChoosePagesState(
        adp, userid, chatid, lang, general_dict, 
        horizontal=2, vertical=3,
        autoanswer=False, one_element=False)