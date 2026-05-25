from refactored_code import *
import pytest
from typing import List, Optional

# Импортируем сам модуль, чтобы протестировать приватные методы (если нужно)
from module_name import (
    DEFAULT_MULTIPLIER,
    f,
    calc,
    process,
    get_user
)

# Тестим функцию f
def test_f():
    assert f(5, 7) == 12
    assert f(-4, 9) == 5
    with pytest.raises(TypeError):
        f('a', 'b')

# Тестим функцию calc
def test_calc():
    # Позитивный сценарий
    assert calc(3, 4, 5) == 9.0
    # Негативный сценарий (деление на ноль)
    with pytest.raises(ValueError):
        calc(0, 0, 1)

# Тестим функцию process
def test_process():
    # Граничные значения
    assert process([0, 1, 2, 3, 4]) == [0, 3, 4, 9, 8]
    # Чётное число в конце
    assert process([1, 2, 3, 4, 6]) == [3, 4, 9, 8, 12]
    # Пустой список
    assert process([]) == []
    # Отрицательные числа
    assert process([-1, -2, -3, -4]) == [-3, -4, -9, -8]

# Тестим функцию get_user
def test_get_user():
    # Позитивные сценарии
    assert get_user(1) == "Alice"
    assert get_user(2) == "Bob"
    # Негативные сценарии
    assert get_user(3) is None
    with pytest.raises(TypeError):
        get_user('abc')