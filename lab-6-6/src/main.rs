struct Product { price: f64 }
struct Item { product: Product, quantity: u32 }
struct Order { items: Vec<Item> }

fn type_safe_calculation(order: &Order) -> f64 {
    // Безопасное преобразование u32 -> f64 и строгая типизация суммы
    order.items.iter()
        .map(|item| item.product.price * f64::from(item.quantity))
        .sum()
}

fn main() {
    let order = Order {
        items: vec![
            Item { product: Product { price: 100.0 }, quantity: 2 },
            Item { product: Product { price: 50.0 }, quantity: 1 },
        ],
    };
    let total = type_safe_calculation(&order);
    println!("Rust: Итоговая сумма (безопасно): {:.2}", total);
}