from dataclasses import dataclass
from typing import List, Dict
import functools

@dataclass
class User:
    id: int
    name: str
    email: str

@dataclass
class Product:
    id: int
    name: str
    price: float
    category: str

@dataclass
class OrderItem:
    product: Product
    quantity: int

@dataclass
class Order:
    id: int
    user: User
    items: List[OrderItem]
    status: str

# Пример данных
users = [
    User(1, "John Doe", "john@example.com"),
    User(2, "Jane Smith", "jane@example.com")
]

products = [
    Product(1, "iPhone", 999.99, "electronics"),
    Product(2, "MacBook", 1999.99, "electronics"),
    Product(3, "T-shirt", 29.99, "clothing")
]

orders = [
    Order(1, users[0], [OrderItem(products[0], 1), OrderItem(products[2], 2)], "completed"),
    Order(2, users[1], [OrderItem(products[1], 1)], "pending")
]

# Функции обработки
def calculate_order_total(order: Order) -> float:
    return sum(item.product.price * item.quantity for item in order.items)

def filter_orders_by_status(orders: List[Order], status: str) -> List[Order]:
    return list(filter(lambda order: order.status == status, orders))

def get_top_expensive_orders(orders: List[Order], n: int) -> List[Order]:
    return sorted(orders, key=calculate_order_total, reverse=True)[:n]

def apply_discount(order: Order, discount: float) -> Order:
    discounted_items = [
        OrderItem(
            Product(
                item.product.id,
                item.product.name,
                item.product.price * (1 - discount),
                item.product.category
            ),
            item.quantity
        ) for item in order.items
    ]
    return Order(order.id, order.user, discounted_items, order.status)

def main():
    completed_orders = filter_orders_by_status(orders, "completed")
    total_revenue = sum(calculate_order_total(order) for order in completed_orders)
    top_orders = get_top_expensive_orders(orders, 2)
    
    print(f"Общая выручка: {total_revenue}")
    print(f"Топ заказы: {[calculate_order_total(order) for order in top_orders]}")

if __name__ == "__main__":
    main()