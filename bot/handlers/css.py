from bot.exec import bot
from bot.modules.tools import ChooseStepState
from bot.modules.markup import list_to_keyboard
from telebot.types import ReplyKeyboardRemove

async def adp(return_data: dict, transmitted_data: dict):
    """ Функция обработки выбранного числа
    """
    userid = transmitted_data['userid']
    
    await bot.send_message(userid, f'Вы ввели `{return_data}`', reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')

@bot.message_handler(commands=['css'])
async def test_css(message):
    userid = message.from_user.id
    chatid = message.chat.id
    lang = message.from_user.language_code

    """ В виде словаря мы вводим какие данные мы хотим получить
        type - 'int' 'str' 'bool' 'option' 'custom' 'pages'
        
        name - имя ключа с данными в конечном словаря НЕ ДОЛЖНЫ ПОВТАРЯТЬСЯ
        
        data - данные для самой функции, следуя из прошлых примеров - минимальная / максимальная длинна текста
        
        message - данные для send_message
    """ 
    
    age_data = {
        'Мужчина': 'male',
        'Женщина': 'female',
        'Ламинат': 'other'
    }
    age_markup = list_to_keyboard([list(age_data.keys()), ["❌ Отмена"]])
    
    steps = [
            {"type": 'str', "name": 'name', "data": {"max_len": 199}, 
                'message': {"text": "Введите своё имя",
                            "reply_markup": list_to_keyboard(["❌ Отмена"])
                            }
            },
            {"type": 'int', "name": 'age', "data": {
                "max_int": 120, "min_int": 1}, 
                'message': {"text": "Введите свой возраст",
                            }
            },
            {"type": 'option', "name": 'gender ', "data": {
                "options": age_data}, 
                'message': {"text": "Выберите свой пол",
                            "reply_markup": age_markup
                            }
            },
            {"type": 'bool', "name": 'confirm ', "data": {}, 
                'message': {"text": "Согласны на обработку данных?",
                            "reply_markup": 
                                list_to_keyboard([["✅ Подтверждаю", "❌ Отмена"]])
                            }
            },
            ]

    await ChooseStepState(
        adp, userid, chatid, lang, steps
        )