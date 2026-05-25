"""
Клиент для работы с GigaChat API
Поддерживает генерацию кода, рефакторинг, создание тестов и документации
"""

import os
import json
from dotenv import load_dotenv
from gigachat import GigaChat
from typing import List, Dict, Optional

# Загрузка переменных окружения
load_dotenv()


class GigaChatAssistant:
    """Ассистент на основе GigaChat для задач разработки"""
    
    def __init__(self):
        self.credentials = os.getenv("GIGACHAT_CREDENTIALS")
        self.scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
        self.model = os.getenv("GIGACHAT_MODEL", "GigaChat-2")
        self.verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "False").lower() == "true"
        
        # Инициализация клиента GigaChat
        self.client = GigaChat(
            credentials=self.credentials,
            scope=self.scope,
            model=self.model,
            verify_ssl_certs=self.verify_ssl
        )
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """Генерация кода по текстовому описанию"""
        prompt = f"""
        Ты — эксперт по разработке на {language}. Напиши код на {language} для следующей задачи:
        
        {description}
        
        Требования к коду:
        - Добавь аннотации типов (для Python)
        - Добавь docstring с описанием функции, параметров и возвращаемого значения
        - Используй понятные имена переменных
        - Добавь обработку ошибок
        
        Верни только код, без пояснений.
        """
        
        response = self.client.chat(prompt)
        code = response.choices[0].message.content
        
        # Очистка от markdown-разметки
        if "```" in code:
            code = code.split("```")[1]
            if code.startswith(language):
                code = code[len(language):]
            code = code.strip()
        
        return code
    
    def refactor_code(self, code: str, requirements: str) -> str:
        """Рефакторинг существующего кода"""
        prompt = f"""
        Проведи рефакторинг следующего кода согласно требованиям.
        
        Исходный код:
        ```python
        {code}
        ```
        
        Требования к рефакторингу:
        {requirements}
        
        Дополнительные требования:
        - Сохрани исходную функциональность
        - Улучши читаемость кода
        - Добавь аннотации типов (если их нет)
        - Разбей на более мелкие функции (если необходимо)
        - Добавь обработку ошибок
        
        Верни только отрефакторенный код, без пояснений.
        """
        
        response = self.client.chat(prompt)
        refactored = response.choices[0].message.content
        
        if "```" in refactored:
            refactored = refactored.split("```")[1]
            if refactored.startswith("python"):
                refactored = refactored[6:]
            refactored = refactored.strip()
        
        return refactored
    
    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """Генерация тестов для кода"""
        prompt = f"""
        Напиши тесты для следующего кода, используя {framework}.
        
        Код для тестирования:
        ```python
        {code}
        ```
        
        Требования к тестам:
        - Протестируй все публичные функции
        - Включи позитивные и негативные сценарии
        - Проверь граничные случаи
        - Добавь понятные названия тестов
        
        Верни только код с тестами, без пояснений.
        """
        
        response = self.client.chat(prompt)
        tests = response.choices[0].message.content
        
        if "```" in tests:
            tests = tests.split("```")[1]
            if tests.startswith("python") or tests.startswith(framework):
                tests = tests.split("\n", 1)[1] if "\n" in tests else tests
            tests = tests.strip()
        
        return tests
    
    def generate_documentation(self, code: str, doc_type: str = "docstring") -> str:
        """Генерация документации для кода"""
        if doc_type == "docstring":
            prompt = f"""
            Добавь docstring для каждой функции в следующем коде.
            
            Код:
            ```python
            {code}
            ```
            
            Формат docstring (Google Style):
            def function(param1: type, param2: type) -> return_type:
                \"\"\"Краткое описание.
                
                Args:
                    param1: Описание параметра 1
                    param2: Описание параметра 2
                
                Returns:
                    Описание возвращаемого значения
                
                Raises:
                    ExceptionType: Когда возникает исключение
                \"\"\"
            
            Верни полный код с добавленными docstring.
            """
        else:
            prompt = f"""
            Создай README документацию для следующего кода.
            
            Код:
            ```python
            {code}
            ```
            
            Включи в документацию:
            - Описание назначения кода
            - Инструкцию по установке зависимостей
            - Примеры использования
            - Описание основных функций
            """
        
        response = self.client.chat(prompt)
        documentation = response.choices[0].message.content
        
        if doc_type == "docstring" and "```" in documentation:
            documentation = documentation.split("```")[1]
            if documentation.startswith("python"):
                documentation = documentation[6:]
            documentation = documentation.strip()
        
        return documentation
    
    def analyze_code(self, code: str) -> Dict[str, List[str]]:
        """Анализ качества, читаемости и потенциальных уязвимостей"""
        prompt = f"""
        Проанализируй следующий код и верни результат в формате JSON.
        
        Код:
        ```python
        {code}
        ```
        
        Оцени следующие аспекты:
        1. quality_issues: проблемы качества кода (нарушения PEP8, длинные функции и т.д.)
        2. readability_issues: проблемы читаемости (плохие имена переменных, отсутствие комментариев)
        3. security_issues: потенциальные уязвимости (инъекции, небезопасные функции)
        4. performance_issues: проблемы производительности (неэффективные алгоритмы)
        5. suggestions: конкретные предложения по улучшению
        
        Формат ответа (JSON):
        {{
            "quality_issues": ["проблема 1", "проблема 2"],
            "readability_issues": ["проблема 1"],
            "security_issues": [],
            "performance_issues": ["проблема 1"],
            "suggestions": ["предложение 1", "предложение 2"]
        }}
        
        Верни ТОЛЬКО JSON, без сопутствующего текста и пояснений.
        """
        
        response = self.client.chat(prompt)
        result = response.choices[0].message.content
        
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0]
        elif "```" in result:
            result = result.split("```")[1]
        
        try:
            return json.loads(result.strip())
        except json.JSONDecodeError:
            return {"error": ["Не удалось распарсить ответ"], "raw_response": result}
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Простой чат с GigaChat"""
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nПользователь: {message}\nАссистент:"
        else:
            full_prompt = message
        
        response = self.client.chat(full_prompt)
        return response.choices[0].message.content


if __name__ == "__main__":
    assistant = GigaChatAssistant()
    print("=== Тест чата ===")
    response = assistant.chat("Привет! Расскажи кратко, что ты умеешь?")
    print(f"Ответ: {response}\n")