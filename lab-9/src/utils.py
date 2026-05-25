import json
from typing import Any

class JsonSerializer:
    """SRP: Отвечает только за сериализацию."""
    @staticmethod
    def to_json(obj: Any) -> str:
        # Упрощенная реализация для примера
        if hasattr(obj, '__dict__'):
            return json.dumps(obj.__dict__, default=lambda o: str(o), indent=4)
        return str(obj)

class Logger:
    """SRP: Логирование."""
    @staticmethod
    def log(message: str):
        print(f"[LOG]: {message}")