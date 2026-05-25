import time
from functools import wraps

# Простой декоратор
def timer(func):
    """Декоратор для измерения времени выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

# Декоратор с параметрами
def repeat(num_times=2):
    """Декоратор для повторного выполнения функции"""
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

# Применение декораторов
@timer
def slow_function():
    """Медленная функция для демонстрации"""
    time.sleep(1)
    return "Готово!"

@repeat(num_times=3)
def greet(name):
    """Функция приветствия"""
    print(f"Привет, {name}!")

# Декоратор для кэширования
def cache(func):
    """Простой декоратор для кэширования"""
    cached_results = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cached_results:
            print(f"Используется кэшированный результат для {args}")
            return cached_results[args]
        result = func(*args)
        cached_results[args] = result
        return result
    return wrapper

@cache
def expensive_operation(x):
    """Дорогая операция"""
    print(f"Вычисление для {x}...")
    time.sleep(0.5)
    return x * x

# Демонстрация работы
print("=== Демонстрация декораторов ===")
slow_function()
greet("Иван")

print("Кэшированные вычисления:")
print(expensive_operation(5))
print(expensive_operation(5))  # Должен использовать кэш
print(expensive_operation(10))