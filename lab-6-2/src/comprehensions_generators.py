# Списковые включения (list comprehensions)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Простые включения
squares = [x * x for x in numbers]
print(f"Квадраты: {squares}")

# Включения с условием
even_squares = [x * x for x in numbers if x % 2 == 0]
print(f"Квадраты четных: {even_squares}")

# Словарные включения
student_dict = {student['name']: student['grade'] for student in students}
print(f"Словарь студентов: {student_dict}")

# Множества (set) включения
unique_ages = {student['age'] for student in students}
print(f"Уникальные возрасты: {unique_ages}")

# Генераторы
def fibonacci_generator(limit):
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Использование генератора
print("Числа Фибоначчи:")
fib_gen = fibonacci_generator(10)
for num in fib_gen:
    print(num, end=" ")
print()

# Генераторные выражения
squares_gen = (x * x for x in numbers)
print(f"Генератор квадратов: {list(squares_gen)}")
