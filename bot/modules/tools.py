from bot.exec import bot
from bot.modules.data_format import chunk_pages
from bot.modules.markup import down_menu, list_to_keyboard
from telebot.asyncio_handler_backends import State, StatesGroup


class GeneralStates(StatesGroup):
    ChooseInt = State() # Состояние для ввода числа
    ChooseString = State() # Состояние для ввода текста
    ChooseConfirm = State() # Состояние для подтверждения (да / нет)
    ChooseOption = State() # Состояние для выбора среди вариантов
    ChoosePagesState = State() # Состояние для выбора среди вариантов, а так же поддерживает страницы
    ChooseCustom = State() # Состояние для кастомного обработчика

def add_if_not(data: dict, userid: int, chatid: int, lang: str):
    """Добавляет минимальные данные для работы"""
    if 'userid' not in data: data['userid'] = userid
    if 'chatid' not in data: data['chatid'] = chatid
    if 'lang' not in data: data['lang'] = lang
    return data

async def ChooseIntState(function, userid: int, 
                chatid: int, lang: str,
                min_int: int = 1, max_int: int = 10,
                transmitted_data=None):
    """ Устанавливает состояние ожидания числа

        В function передаёт 
        >>> number: int, transmitted_data: dict
        
        Если max_int == 0, значит нет ограничения.
        
        Return:
         Возвращает True если был создано состояние, False если завершилось автоматически (минимальный и максимальный вариант совпадают)
    """
    
    if not transmitted_data: transmitted_data = {}
    transmitted_data = add_if_not(transmitted_data, userid, chatid, lang)
    
    if min_int != max_int:
        await bot.set_state(userid, GeneralStates.ChooseInt, chatid)
        async with bot.retrieve_data(userid, chatid) as data:
            data['function'] = function
            data['transmitted_data'] = transmitted_data
            data['min_int'] = min_int
            data['max_int'] = max_int
        return True, 'int'
    else:
        await function(min_int, transmitted_data)
        return False, 'int'

async def ChooseStringState(function, userid: int, 
                         chatid: int, lang: str,
                         min_len: int = 1, max_len: int = 10,
                         transmitted_data=None):
    """ Устанавливает состояние ожидания сообщения

        В function передаёт 
        >>> string: str, transmitted_data: dict
        
        Return:
         Возвращает True если был создано состояние, не может завершится автоматически
    """
    if not transmitted_data: transmitted_data = {}
    
    transmitted_data = add_if_not(transmitted_data, userid, chatid, lang)
    await bot.set_state(userid, GeneralStates.ChooseString, chatid)
    async with bot.retrieve_data(userid, chatid) as data:
        data['function'] = function
        data['transmitted_data'] = transmitted_data
        data['min_len'] = min_len
        data['max_len'] = max_len
    return True, 'string'

async def ChooseConfirmState(function, userid: int, 
                         chatid: int, lang: str, cancel: bool=False,
                         transmitted_data=None):
    """ Устанавливает состояние ожидания подтверждения действия

        В function передаёт 
        >>> answer: bool, transmitted_data: dict
        
        cancel - если True, то при отказе вызывает возврат в меню
        
        Return:
         Возвращает True если был создано состояние, не может завершится автоматически
    """
    if not transmitted_data: transmitted_data = {}
    transmitted_data['cancel'] = cancel
    
    transmitted_data = add_if_not(transmitted_data, userid, chatid, lang)
    await bot.set_state(userid, GeneralStates.ChooseConfirm, chatid)
    async with bot.retrieve_data(userid, chatid) as data:
        data['function'] = function
        data['transmitted_data'] = transmitted_data
    return True, 'confirm'

async def ChooseOptionState(function, userid: int, 
                         chatid: int, lang: str,
                         options: dict = {},
                         transmitted_data=None):
    """ Устанавливает состояние ожидания выбора опции

        В function передаёт 
        >>> answer: ???, transmitted_data: dict
        
        Return:
         Возвращает True если был создано состояние, False если завершилось автоматически (1 вариант выбора)
    """
    if not transmitted_data: transmitted_data = {}
    transmitted_data = add_if_not(transmitted_data, userid, chatid, lang)
    
    if len(options) > 1:
        await bot.set_state(userid, GeneralStates.ChooseOption, chatid)
        async with bot.retrieve_data(userid, chatid) as data:
            data['function'] = function
            data['transmitted_data'] = transmitted_data
            data['options'] = options
        return True, 'option'
    else:
        element = options[list(options.keys())[0]]
        await function(element, transmitted_data)
        return False, 'option'
    
async def ChooseCustomState(function, custom_handler, 
                         userid: int, 
                         chatid: int, lang: str,
                         transmitted_data=None):
    """ Устанавливает состояние ожидания чего либо, все проверки идут через custom_handler
    
        custom_handler -> bool, Any !
        в custom_handler передаётся (Message, transmitted_data)

        В function передаёт 
        >>> answer: ???, transmitted_data: dict
        
        Return:
         result - второе возвращаемое из custom_handler
    """
    if not transmitted_data: transmitted_data = {}
    transmitted_data = add_if_not(transmitted_data, userid, chatid, lang)

    await bot.set_state(userid, GeneralStates.ChooseCustom, chatid)
    async with bot.retrieve_data(userid, chatid) as data:
        data['function'] = function
        data['transmitted_data'] = transmitted_data
        data['custom_handler'] = custom_handler
    return True, 'custom'

async def update_page(pages: list, page: int, chat_id: int, lang: str):
    """ Стандарнтная функция, вызывающаяся при обработке страницы
    """
    # Создаёт клавиатуру
    keyboard = list_to_keyboard(pages[page])
    # Добавляет стрелочки и кнопку отмены
    keyboard = down_menu(keyboard, len(pages) > 1, lang)
    await bot.send_message(chat_id, "🎏 Страница обновлена", reply_markup=keyboard)

async def ChoosePagesState(function, userid: int, 
                         chatid: int, lang: str,
                         options: dict = {}, 
                         horizontal: int=2, vertical: int=3,
                         transmitted_data=None, 
                         autoanswer: bool = True, one_element: bool = True,
                         update_page_function = update_page):
    """ Устанавливает состояние ожидания выбора опции
    
        options = {
            'button_name': data
        }
        
        autoanswer - надо ли делать авто ответ, при 1-ом варианте
        horizontal, vertical - размер страницы
        one_element - будет ли завершаться работа после выбора одного элемента

        В function передаёт 
        >>> answer: ???, transmitted_data: dict
            return 
               - если не требуется ничего обновлять, можно ничего не возвращать.
               - если требуется после какого то элемента удалить состояние - {'status': 'reset'}
               - если требуется обновить страницу с переданнами данными - {'status': 'update', 'options': {}} (по желанию ключ 'page')
               - если требуется удалить или добавить элемент, при этом обновив страницу 
               {'status': 'edit', 'elements': {'add' | 'delete': data}}
                 - 'add' - в data требуется передать словарь с ключами, данные объединяются
                 - 'delete' - в data требуется передать список с ключами, ключи будут удалены
        
        В update_page_function передаёт 
        >>> pages: list, page: int, chat_id: int, lang: str
        
        Return:
         Возвращает True если был создано состояние, False если завершилось автоматически (1 вариант выбора)
    """
    if not transmitted_data: transmitted_data = {}
    transmitted_data = add_if_not(transmitted_data, userid, chatid, lang)
    
    # Чанкует страницы и добавляем пустые элементы для сохранения структуры
    pages = chunk_pages(options, horizontal, vertical)
    
    if len(options) > 1 or not autoanswer:
        await bot.set_state(userid, GeneralStates.ChoosePagesState, chatid)
        async with bot.retrieve_data(userid, chatid) as data:
            data['function'] = function
            data['update_page'] = update_page_function
            
            data['transmitted_data'] = transmitted_data
            data['options'] = options
            data['pages'] = pages
            
            data['page'] = 0
            data['one_element'] = one_element
            
            data['settings'] = {'horizontal': horizontal, "vertical": vertical}

        await update_page_function(pages, 0, chatid, lang)
        return True, 'optionplus', pages
    else:
        if len(options) == 0: element = None
        else: element = options[list(options.keys())[0]]

        await function(element, transmitted_data)
        return False, 'optionplus', pages

async def ChooseStepState(function, userid: int, 
                         chatid: int, lang: str,
                         steps: list = [],
                         transmitted_data=None):
    """ Конвеерная Система Состояний
        Устанавливает ожидание нескольких ответов, запуская состояния по очереди.
        
        steps = [
            {"type": str, "name": str, "data": dict, 
                'message': {'text': str, 'reply_markup': markup}}
        ]
        type - тип опроса пользователя (chooses)
        name - имя ключа в возвращаемом инвентаре (не повторять для корректности)
        data - данные для функции создания опроса
        message - данные для отправляемо сообщения перед опросом

        В function передаёт 
        >>> answer: dict, transmitted_data: dict
    """
    if not transmitted_data: transmitted_data = {}
    
    chooses = {
        'int': ChooseIntState,
        'str': ChooseStringState,
        'bool': ChooseConfirmState,
        'option': ChooseOptionState,
        'pages': ChoosePagesState,
        'custom': ChooseCustomState,
    }
    for step in steps:
        if step['type'] in chooses:
            step['function'] = chooses[step['type']]
            
            step['data'] = dict(add_if_not(
                step['data'], userid, chatid, lang))
        else:
            steps.remove(step)
    
    transmitted_data = dict(add_if_not(transmitted_data, 
                            userid, chatid, lang))
    
    transmitted_data['steps'] = steps
    transmitted_data['return_function'] = function
    transmitted_data['return_data'] = {}
    await next_step(0, transmitted_data, True)


# Должен быть ниже всех других обработчиков, 
# для возможности их использования
async def next_step(answer, transmitted_data: dict, start: bool=False):
    """Обработчик КСС*

    Args:
        answer (_type_): Ответ переданный из функции ожидания
        transmitted_data (dict): Переданная дата
        start (bool, optional): Является ли функция стартом КСС Defaults to False.
    """
    userid = transmitted_data['userid']
    chatid = transmitted_data['chatid']
    
    steps = transmitted_data['steps']
    return_data = transmitted_data['return_data']

    # Обновление внутренних данных
    if not start:
        name = steps[len(return_data)]['name']
        if name:
            transmitted_data['return_data'][name] = answer

    if len(return_data) != len(steps): #Получение данных по очереди
        ret_data = steps[len(return_data)]

        # Следующая функция по счёту
        func_answer, func_type = await ret_data['function'](next_step, 
                    transmitted_data=transmitted_data, **ret_data['data']
        )
        # Отправка если состояние было добавлено и не была завершена автоматически
        if func_type == 'cancel':
            # Если функция возвращает не свой тип, а "cancel" - её надо принудительно завершить
            await bot.delete_state(userid, chatid)
            await bot.reset_data(userid, chatid)
        if func_answer:
            # Отправка сообщения из message: dict, если None - ничего
            if ret_data['message']:
                await bot.send_message(userid, parse_mode='Markdown', **ret_data['message'])
        # Обновление данных состояния
        if not start and func_answer:
            async with bot.retrieve_data(userid, chatid) as data:
                data['transmitted_data'] = transmitted_data

    else: #Все данные получены
        await bot.delete_state(userid, chatid)
        await bot.reset_data(userid, chatid)

        return_function = transmitted_data['return_function']
        del transmitted_data['steps']
        del transmitted_data['return_function']
        del transmitted_data['return_data']

        await return_function(return_data, transmitted_data)