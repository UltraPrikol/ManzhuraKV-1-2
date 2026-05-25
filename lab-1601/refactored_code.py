from typing import List, Optional

DEFAULT_MULTIPLIER = 100

def f(x: int, y: int) -> int:
    """Возвращает сумму двух целых чисел."""
    return x + y


def calc(a: int, b: int, c: int) -> float:
    """
    Вычисляет среднее арифметическое произведения a и b плюс число c.
    
    :param a: целое число
    :param b: целое число
    :param c: целое число
    :return: вещественное число
    """
    try:
        res1 = a * b
        res2 = res1 + c
        result = res2 / 2
        return result
    except ZeroDivisionError:
        raise ValueError("Деление на ноль невозможно")


def process(lst: List[int]) -> List[int]:
    """
    Применяет умножение на два к чётным числам списка и умножение на три — к нечётным.
    
    :param lst: список целых чисел
    :return: новый список преобразованных чисел
    """
    result = []
    for num in lst:
        if num % 2 == 0:
            result.append(num * 2)
        else:
            result.append(num * 3)
    return result


def get_user(id_: int) -> Optional[str]:
    """
    Возвращает имя пользователя по идентификатору.
    
    :param id_: целочисленный идентификатор пользователя
    :return: строка имени пользователя или None, если идентификатор неверный
    """
    if id_ == 1:
        return "Alice"
    elif id_ == 2:
        return "Bob"
    else:
        return None