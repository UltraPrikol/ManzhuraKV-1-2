import json
from gigachat_client import GigaChatAssistant

assistant = GigaChatAssistant()

# 1. Читаем плохой код
print("Читаем bad_code.py...")
with open("bad_code.py", "r", encoding="utf-8") as f:
    bad_code = f.read()

# 2. Делаем рефакторинг
print("Запускаем рефакторинг через ИИ...")
requirements = """
1. ВНИМАНИЕ: Имена исходных функций (f, calc, process, get_user) ОСТАВЬ БЕЗ ИЗМЕНЕНИЙ! Переименовывай только аргументы и внутренние переменные по PEP8.
2. Добавь аннотации типов для всех аргументов и возвращаемых значений (используй int для id в get_user).
3. Добавь Google Style docstring для каждой функции.
4. Замени глобальную переменную 'g' на константу DEFAULT_MULTIPLIER = 100.
5. Добавь обработку ошибок (например, ValueError или TypeError) в функции, где это уместно.
"""
refactored = assistant.refactor_code(bad_code, requirements=requirements)

with open("refactored_code.py", "w", encoding="utf-8") as f:
    f.write(refactored)
print("Отрефакторенный код сохранен в refactored_code.py!")

print("Генерируем модульные тесты...")
tests = assistant.generate_tests(refactored, framework="pytest")

tests = tests.replace("main_module", "refactored_code")
tests = tests.replace("bad_code", "refactored_code")

if "refactored_code" not in tests:
    tests = "from refactored_code import *\n" + tests

with open("test_refactored.py", "w", encoding="utf-8") as f:
    f.write(tests)
print("Тесты сохранены в test_refactored.py с автоматическим исправлением импортов!")