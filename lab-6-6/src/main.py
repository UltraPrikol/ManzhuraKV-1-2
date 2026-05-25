import timeit

class Product:
    def __init__(self, price): self.price = price

class Item:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

def calculate_order_total(items):
    return sum(item.product.price * item.quantity for item in items)

# Подготовка данных
orders_data = [[Item(Product(100.0), 2), Item(Product(50.0), 1)] for _ in range(100)]

def benchmark_python():
    # Замер 1000 циклов обработки 100 заказов
    total_time = timeit.timeit(lambda: [calculate_order_total(order) for order in orders_data], number=1000)
    print(f"Python: Время выполнения 1000 итераций: {total_time:.4f} сек")

benchmark_python()