#[derive(Debug, Clone)]
struct User {
    id: u32,
    name: String,
    email: String,
}

#[derive(Debug, Clone)]
struct Product {
    id: u32,
    name: String,
    price: f64,
    category: String,
}

#[derive(Debug, Clone)]
struct OrderItem {
    product: Product,
    quantity: u32,
}

#[derive(Debug, Clone)]
struct Order {
    id: u32,
    user: User,
    items: Vec<OrderItem>,
    status: String,
}

impl User {
    fn new(id: u32, name: &str, email: &str) -> Self {
        User {
            id,
            name: name.to_string(),
            email: email.to_string(),
        }
    }
}

impl Product {
    fn new(id: u32, name: &str, price: f64, category: &str) -> Self {
        Product {
            id,
            name: name.to_string(),
            price,
            category: category.to_string(),
        }
    }
}

impl OrderItem {
    fn new(product: Product, quantity: u32) -> Self {
        OrderItem { product, quantity }
    }
}

impl Order {
    fn new(id: u32, user: User, items: Vec<OrderItem>, status: &str) -> Self {
        Order {
            id,
            user,
            items,
            status: status.to_string(),
        }
    }
}

// Функции обработки
fn calculate_order_total(order: &Order) -> f64 {
    order.items.iter()
        .map(|item| item.product.price * item.quantity as f64)
        .sum()
}

fn filter_orders_by_status(orders: &[Order], status: &str) -> Vec<Order> {
    orders.iter()
        .filter(|order| order.status == status)
        .cloned()
        .collect()
}

fn get_top_expensive_orders(orders: &[Order], n: usize) -> Vec<Order> {
    let mut sorted_orders = orders.to_vec();
    sorted_orders.sort_by(|a, b| {
        calculate_order_total(b).partial_cmp(&calculate_order_total(a)).unwrap()
    });
    sorted_orders.into_iter().take(n).collect()
}

fn apply_discount(order: &Order, discount: f64) -> Order {
    let discounted_items: Vec<OrderItem> = order.items.iter()
        .map(|item| {
            let discounted_product = Product {
                price: item.product.price * (1.0 - discount),
                ..item.product.clone()
            };
            OrderItem {
                product: discounted_product,
                ..item.clone()
            }
        })
        .collect();
    
    Order {
        items: discounted_items,
        ..order.clone()
    }
}

fn main() {
    let users = vec![
        User::new(1, "John Doe", "john@example.com"),
        User::new(2, "Jane Smith", "jane@example.com"),
    ];
    
    let products = vec![
        Product::new(1, "iPhone", 999.99, "electronics"),
        Product::new(2, "MacBook", 1999.99, "electronics"),
        Product::new(3, "T-shirt", 29.99, "clothing"),
    ];
    
    let orders = vec![
        Order::new(
            1, 
            users[0].clone(), 
            vec![
                OrderItem::new(products[0].clone(), 1),
                OrderItem::new(products[2].clone(), 2)
            ], 
            "completed"
        ),
        Order::new(
            2, 
            users[1].clone(), 
            vec![
                OrderItem::new(products[1].clone(), 1)
            ], 
            "pending"
        ),
    ];
    
    let completed_orders = filter_orders_by_status(&orders, "completed");
    let total_revenue: f64 = completed_orders.iter().map(calculate_order_total).sum();
    let top_orders = get_top_expensive_orders(&orders, 2);
    
    println!("Общая выручка: {:.2}", total_revenue);
    println!("Топ заказы: {:?}", top_orders.iter().map(calculate_order_total).collect::<Vec<f64>>());
}