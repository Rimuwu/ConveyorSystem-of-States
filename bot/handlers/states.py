
from bot.exec import bot
from bot.modules.data_format import chunk_pages
from bot.modules.markup import markups_menu as m
from bot.modules.tools import GeneralStates
from telebot.types import Message

back_button = "◀"
forward_button = "▶"

async def cancel(message, text:str = "❌"):
    """ Функция отмены, срабатывает при отмене 
    """
    if text:
        await bot.send_message(message.chat.id, text, 
            reply_markup=m(message.from_user.id, 'last_menu', 
                           message.from_user.language_code))
    await bot.delete_state(message.from_user.id, message.chat.id)
    await bot.reset_data(message.from_user.id,  message.chat.id)

@bot.message_handler(text='❌ Отмена', state='*')
async def cancel_m(message: Message):
    """Состояние отмены
    """
    await cancel(message)

@bot.message_handler(commands=['cancel'], state='*')
async def cancel_c(message: Message):
    """Команда отмены
    """
    await cancel(message)


@bot.message_handler(commands=['state'])
async def get_state(message: Message):
    """Состояние
    """
    state = await bot.get_state(message.from_user.id, message.chat.id)
    await bot.send_message(message.chat.id, f'{state}')
    try:
        async with bot.retrieve_data(message.from_user.id, 
                                 message.chat.id) as data: print(data)
    except: pass

@bot.message_handler(state=GeneralStates.ChooseInt)
async def ChooseInt(message: Message):
    """Общая функция для ввода числа,
       Поддерживает варианты ввода - 
        1. Сообщение - число
        2. текстчисло, пример "х100"
       Ищет пока не найдёт
    """
    userid = message.from_user.id
    lang = message.from_user.language_code
    number = 0

    async with bot.retrieve_data(userid, message.chat.id) as data:
        min_int: int = data['min_int']
        max_int: int = data['max_int']
        func = data['function']
        transmitted_data = data['transmitted_data']

    for iter_word in str(message.text).split():
        if iter_word.isdigit():
            number = int(iter_word)

        elif iter_word.startswith('x') and \
            iter_word[1:].isdigit():
            number = int(iter_word[1:])

    if not number:
        await bot.send_message(message.chat.id, 
                "Не число")
    elif max_int != 0 and number > max_int:
        await bot.send_message(message.chat.id, 
                f"Больше максимума ({number} > {max_int})")
    elif number < min_int:
        await bot.send_message(message.chat.id, 
                f"Меньше минимума ({number} < {min_int})")
    else:
        await bot.delete_state(userid, message.chat.id)
        await bot.reset_data(message.from_user.id,  message.chat.id)
        await func(number, transmitted_data=transmitted_data)

@bot.message_handler(state=GeneralStates.ChooseString)
async def ChooseString(message: Message):
    """Общая функция для ввода сообщения
    """
    userid = message.from_user.id
    lang = message.from_user.language_code

    async with bot.retrieve_data(userid, message.chat.id) as data:
        max_len: int = data['max_len']
        min_len: int = data['min_len']
        func = data['function']
        transmitted_data = data['transmitted_data']

    content = str(message.text)
    content_len = len(content)

    if content_len > max_len:
        await bot.send_message(message.chat.id, 
                f"Длинна больше максимума ({content_len} > {max_len}")
    elif content_len < min_len:
        await bot.send_message(message.chat.id, 
                f"Длинна меньшк минимума ({content_len} < {min_len})")
    else:
        await bot.delete_state(userid, message.chat.id)
        await bot.reset_data(message.from_user.id,  message.chat.id)
        await func(content, transmitted_data=transmitted_data)

@bot.message_handler(state=GeneralStates.ChooseConfirm)
async def ChooseConfirm(message: Message):
    """Общая функция для подтверждения
    """
    userid = message.from_user.id
    lang = message.from_user.language_code
    content = str(message.text)

    async with bot.retrieve_data(userid, message.chat.id) as data:
        func = data['function']
        transmitted_data = data['transmitted_data']
        cancel_status = transmitted_data['cancel']

    buttons_data = {
        "✅ Включить": True,
        "✅ Подтверждаю": True,
        "❌ Выключить": False
    }
    
    if content in buttons_data:
        if not(buttons_data[content]) and cancel_status:
            await cancel(message)
        else:
            await bot.delete_state(userid, message.chat.id)
            await bot.reset_data(message.from_user.id,  message.chat.id)
            await func(buttons_data[content], transmitted_data=transmitted_data)
    else:
        await bot.send_message(message.chat.id, 
                "Ответ - не подтверждение")

@bot.message_handler(state=GeneralStates.ChooseOption)
async def ChooseOption(message: Message):
    """Общая функция для выбора из предложенных вариантов
    """
    userid = message.from_user.id
    lang = message.from_user.language_code

    async with bot.retrieve_data(userid, message.chat.id) as data:
        options: dict = data['options']
        func = data['function']
        transmitted_data = data['transmitted_data']

    if message.text in options.keys():
        await bot.delete_state(userid, message.chat.id)
        await bot.reset_data(message.from_user.id,  message.chat.id)
        await func(options[message.text], transmitted_data=transmitted_data)
    else:
        await bot.send_message(message.chat.id, 
                "Ответа нет в предложенных опциях")

@bot.message_handler(state=GeneralStates.ChooseCustom)
async def ChooseCustom(message: Message):
    """Кастомный обработчик, принимает данные и отправляет в обработчик
    """
    userid = message.from_user.id

    async with bot.retrieve_data(userid, message.chat.id) as data:
        custom_handler = data['custom_handler']
        func = data['function']
        transmitted_data = data['transmitted_data']

    result, answer = await custom_handler(message, transmitted_data) # Обязан возвращать bool, Any
    
    if result:
        await bot.delete_state(userid, message.chat.id)
        await bot.reset_data(message.from_user.id,  message.chat.id)
        await func(answer, transmitted_data=transmitted_data)
    
@bot.message_handler(state=GeneralStates.ChoosePagesState)
async def ChooseOptionPlus(message: Message):
    """Кастомный обработчик, принимает данные и отправляет в обработчик
    """
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code

    async with bot.retrieve_data(userid, message.chat.id) as data:
        func = data['function']
        update_page = data['update_page']

        options: dict = data['options']
        transmitted_data: dict = data['transmitted_data']

        pages: list = data['pages']
        page: int = data['page']
        one_element: bool = data['one_element']
        
        settings: dict = data['settings']

    if message.text in options.keys():
        if one_element:
            await bot.delete_state(userid, message.chat.id)
            await bot.reset_data(message.from_user.id,  message.chat.id)

        transmitted_data['options'] = options
        transmitted_data['key'] = message.text
        res = await func(
            options[message.text], transmitted_data=transmitted_data)

        if not one_element and res and type(res) == dict and 'status' in res:
            # Удаляем состояние
            if res['status'] == 'reset':
                await bot.delete_state(userid, message.chat.id)
                await bot.reset_data(message.from_user.id,  message.chat.id)

            # Обновить все данные
            elif res['status'] == 'update' and 'options' in res:
                pages = chunk_pages(res['options'], settings['horizontal'], settings['vertical'])
                
                if 'page' in res: page = res['page']
                if page >= len(pages) - 1: page = 0

                async with bot.retrieve_data(userid, message.chat.id) as data:
                    data['options'] = res['options']
                    data['pages'] = pages
                    data['page'] = page

                await update_page(pages, page, chatid, lang)

            # Добавить или удалить элемент
            elif res['status'] == 'edit' and 'elements' in res:
                
                for key, value in res['elements'].items():
                    if key == 'add':
                        for iter_key, iter_value in value.items():
                            options[iter_key] = iter_value
                    elif key == 'delete':
                        for i in value: del options[i]

                pages = chunk_pages(options, settings['horizontal'], settings['vertical'])

                if page >= len(pages) - 1: page = 0

                async with bot.retrieve_data(userid, message.chat.id) as data:
                    data['options'] = options
                    data['pages'] = pages
                    data['page'] = page

                await update_page(pages, page, chatid, lang)

    elif message.text == back_button and len(pages) > 1:
        if page == 0: page = len(pages) - 1
        else: page -= 1

        async with bot.retrieve_data(userid, chatid) as data: data['page'] = page
        await update_page(pages, page, chatid, lang)

    elif message.text == forward_button and len(pages) > 1:
        if page >= len(pages) - 1: page = 0
        else: page += 1

        async with bot.retrieve_data(userid, chatid) as data: data['page'] = page
        await update_page(pages, page, chatid, lang)
    else:
        await bot.send_message(message.chat.id, 
                "Ответа нет в предложенных опциях")