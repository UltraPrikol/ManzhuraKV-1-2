// Модель данных
class User {
    constructor(id, name, email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
}

class Product {
    constructor(id, name, price, category) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.category = category;
    }
}

class OrderItem {
    constructor(product, quantity) {
        this.product = product;
        this.quantity = quantity;
    }
}

class Order {
    constructor(id, user, items, status) {
        this.id = id;
        this.user = user;
        this.items = items;
        this.status = status;
    }
}

// Пример данных
const users = [
    new User(1, "John Doe", "john@example.com"),
    new User(2, "Jane Smith", "jane@example.com")
];

const products = [
    new Product(1, "iPhone", 999.99, "electronics"),
    new Product(2, "MacBook", 1999.99, "electronics"),
    new Product(3, "T-shirt", 29.99, "clothing")
];

const orders = [
    new Order(1, users[0], [
        new OrderItem(products[0], 1),
        new OrderItem(products[2], 2)
    ], "completed"),
    new Order(2, users[1], [
        new OrderItem(products[1], 1)
    ], "pending")
];

// Функции обработки
const calculateOrderTotal = (order) => 
    order.items.reduce((total, item) => total + (item.product.price * item.quantity), 0);

const filterOrdersByStatus = (orders, status) => 
    orders.filter(order => order.status === status);

const getTopExpensiveOrders = (orders, n) => 
    [...orders].sort((a, b) => calculateOrderTotal(b) - calculateOrderTotal(a)).slice(0, n);

const applyDiscount = (order, discount) => {
    const discountedItems = order.items.map(item => ({
        ...item,
        product: {
            ...item.product,
            price: item.product.price * (1 - discount)
        }
    }));
    return { ...order, items: discountedItems };
};

// Основная функция
const main = () => {
    const completedOrders = filterOrdersByStatus(orders, "completed");
    const totalRevenue = completedOrders.reduce((sum, order) => sum + calculateOrderTotal(order), 0);
    const topOrders = getTopExpensiveOrders(orders, 2);
    
    console.log("Общая выручка:", totalRevenue);
    console.log("Топ заказы:", topOrders.map(calculateOrderTotal));
};

main();