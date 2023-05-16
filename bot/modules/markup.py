from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

back_button = "◀"
forward_button = "▶"

def markups_menu(userid: int, key: str, lang: str):
    """ Система меню клавиатур, тут можно либо подвязать базу, и по определённому ключу возвращать прошлую клавиатуру, либо вообще убрать и просто удалять клаву.
    """
    return ReplyKeyboardRemove()

def down_menu(markup: ReplyKeyboardMarkup, 
              arrows: bool = True, lang: str = 'en'): 
    """Добавления нижнего меню для страничных клавиатур
    """
    if arrows:
        markup.add(*[back_button, "❌ Отмена", forward_button])
    else: markup.add("❌ Отмена")
    
    return markup

def list_to_keyboard(buttons: list, row_width: int = 3, resize_keyboard: bool = True, one_time_keyboard = None) -> ReplyKeyboardMarkup:
    '''Превращает список со списками в объект клавиатуры.
        Example:
            butttons = [ ['привет'], ['отвяжись', 'ты кто?'] ]

        >      привет
          отвяжись  ты кто?
        
            butttons = ['привет','отвяжись','ты кто?'], 
            row_width = 1

        >  привет
          отвяжись  
          ты кто?
    '''
    markup = ReplyKeyboardMarkup(row_width=row_width, 
                                 resize_keyboard=resize_keyboard, 
                                 one_time_keyboard=one_time_keyboard)
    
    for line in buttons:
        try:
            if type(line) == list:
                markup.add(*[i for i in line])
            else:
                markup.add(line)
        except Exception as e:
            print('list_to_keyboard', line, type(line), e)
    return markup