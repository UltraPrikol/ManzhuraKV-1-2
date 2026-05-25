from functools import reduce, wraps

# =========================
# ЗАДАНИЕ 1
# Анализ данных студентов
# =========================

def analyze_students(students):
    """Анализ данных студентов"""
    total_students = len(students)

    grades = list(map(lambda s: s["grade"], students))

    average_grade = (
        reduce(lambda a, b: a + b, grades, 0) / total_students
        if total_students > 0 else 0
    )

    top_students = list(
        map(
            lambda s: s["name"],
            filter(lambda s: s["grade"] >= 90, students)
        )
    )

    return {
        "average_grade": average_grade,
        "top_students": top_students,
        "total_students": total_students
    }


# =========================
# ЗАДАНИЕ 2
# Декоратор логирования
# =========================

def logger(func):
    """Декоратор для логирования"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Функция: {func.__name__}")
        print(f"[LOG] Аргументы: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] Результат: {result}")
        return result
    return wrapper


@logger
def greet(name):
    return f"Привет, {name}!"


# =========================
# ЗАДАНИЕ 3
# Генератор простых чисел
# =========================

def prime_generator():
    """Генератор простых чисел"""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    number = 2
    while True:
        if is_prime(number):
            yield number
        number += 1


# =========================
# DEMO / main
# =========================

def main():
    print("=== Анализ студентов ===")
    students = [
        {"name": "Анна", "grade": 95},
        {"name": "Иван", "grade": 82},
        {"name": "Мария", "grade": 90},
        {"name": "Петр", "grade": 76},
    ]

    stats = analyze_students(students)
    print(stats)

    print("\n=== Декораторы ===")
    greet("Мария")

    print("\n=== Генератор простых чисел ===")
    primes = prime_generator()
    for _ in range(10):
        print(next(primes), end=" ")
    print()


if __name__ == "__main__":
    main()
