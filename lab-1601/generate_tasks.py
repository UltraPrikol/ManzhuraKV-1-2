from gigachat_client import GigaChatAssistant

assistant = GigaChatAssistant()

print("Генерация функций через GigaChat...")

description_1 = "Напиши функцию validate_email(email: str) -> bool, которая проверяет корректность email-адреса с помощью регулярных выражений и базовой проверки структуры домена."
description_2 = "Напиши функцию sort_by_key(data: list[dict], key: str, reverse: bool = False) -> list[dict], которая сортирует список словарей по заданному ключу с обработкой отсутствия ключа."
description_3 = "Напиши декоратор timer(func), который измеряет время выполнения функции в секундах и выводит его в консоль."

code_1 = assistant.generate_code(description_1)
code_2 = assistant.generate_code(description_2)
code_3 = assistant.generate_code(description_3)

full_generated_code = f"""# Автоматически сгенерированный код через GigaChat API
import time
import re
from typing import List, Dict, Any

{code_1}

{code_2}

{code_3}
"""

with open("generated_code.py", "w", encoding="utf-8") as f:
    f.write(full_generated_code)

print("Все три функции сгенерированы и сохранены в generated_code.py!")