def validate_email(email: str) -> bool:
    """
    Проверяет валидность email-адреса с использованием регулярного выражения.
    
    Параметры:
    email (str): строка, представляющая адрес электронной почты

    Возвращаемое значение:
    bool: True, если email является валидным, иначе False
    """
    import re

    # Регулярное выражение для проверки email-адреса согласно стандарту RFC-5322
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    try:
        return bool(re.fullmatch(pattern, email))
    except TypeError:
        raise ValueError("Передан некорректный тип параметра")

from typing import List, Dict

def sort_by_key(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
    """
    Сортирует список словарей по указанному ключу.
    
    Параметры:
    data (List[Dict]): Список словарей для сортировки
    key (str): Ключ, по которому нужно отсортировать данные
    reverse (bool, optional): Если True, выполняется сортировка в обратном порядке (по умолчанию False)
    
    Возвращаемое значение:
    List[Dict]: Отсортированный список словарей
    
    Исключение:
    KeyError: Если указанный ключ отсутствует хотя бы в одном словаре
    TypeError: Если данные переданы некорректного типа
    """
    # Проверка корректности входных данных
    if not isinstance(data, list):
        raise TypeError("Первый аргумент должен быть списком")
    for item in data:
        if not isinstance(item, dict):
            raise TypeError("Элементы списка должны быть словарями")
    
    try:
        return sorted(data, key=lambda x: x.get(key), reverse=reverse)
    except KeyError as e:
        raise KeyError(f"Ключ '{key}' отсутствует в одном из словарей") from e

from typing import Callable
import time

def timer(func: Callable) -> Callable:
    """
    Декоратор для измерения времени выполнения функции.
    
    Параметры:
    func (Callable): Функция, время выполнения которой нужно измерить
    
    Возвращаемое значение:
    Callable: Декорированная функция с добавлением измерения времени исполнения
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка во время вызова декорированной функции: {e}")
            return None
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения функции '{func.__name__}' составило: {execution_time:.4f} секунд")
        return result
    return wrapper