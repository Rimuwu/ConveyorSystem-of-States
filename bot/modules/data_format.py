""" Функции работы с данными
"""

def chunks(lst: list, n: int) -> list:
    """Делит список lst, на списки по n элементов
       Возвращает список
    """
    def work():
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    return list(work())

def filling_with_emptiness(lst: list, horizontal: int, vertical: int):
    """ Заполняет пустые элементы страницы для сохранения структуры
    """
    for i in lst:
        if len(i) != vertical:
            for _ in range(vertical - len(i)):
                i.append([' ' for _ in range(horizontal)])
    return lst

def chunk_pages(options: dict, horizontal: int=2, vertical: int=3):
    """Чанкует страницы и добавляем пустые элементы для сохранения структуры
    """
    if options:
        pages = chunks(chunks(list(options.keys()), horizontal), vertical)
    else: pages = [[]]
    pages = filling_with_emptiness(pages, horizontal, vertical)
    return pages