#[derive(Debug)]
struct Product {
    name: String,
    price: f64,
    available: bool,
}

#[derive(Debug)]
struct Order {
    id: u32,
    amount: f64,
}

#[derive(Debug)]
enum OrderError {
    InvalidAmount(u32),
}

// --- Задание 1: Анализ продуктов ---
fn analyze_products(products: &[Product]) -> (f64, usize, Vec<&Product>) {
    let count = products.len();
    
    // Средняя цена (если список пуст, вернем 0.0)
    let avg_price = if count == 0 {
        0.0
    } else {
        products.iter().map(|p| p.price).sum::<f64>() / count as f64
    };

    // Количество доступных
    let available_count = products.iter().filter(|p| p.available).count();

    // Список дорогих продуктов (> 100)
    let expensive_products: Vec<&Product> = products
        .iter()
        .filter(|p| p.price > 100.0)
        .collect();

    (avg_price, available_count, expensive_products)
}

// --- Задание 2: Валидация цепочки заказов ---
fn validate_orders(orders: &[Order]) -> Result<Vec<&Order>, OrderError> {
    // В Rust метод collect может превратить Iterator<Result<T, E>> в Result<Vec<T>, E>
    // Он вернет первую встреченную ошибку или вектор всех успешных элементов.
    orders.iter()
        .map(|o| {
            if o.amount > 0.0 {
                Ok(o)
            } else {
                Err(OrderError::InvalidAmount(o.id))
            }
        })
        .collect()
}

// --- Задание 3: Итератор Фибоначчи ---
struct Fibonacci {
    current: u64,
    next: u64,
}

impl Fibonacci {
    fn new() -> Self {
        Fibonacci { current: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        let current_val = self.current;
        
        // Математическая логика: F(n) = F(n-1) + F(n-2)
        let next_val = self.current.checked_add(self.next);
        
        match next_val {
            Some(sum) => {
                self.current = self.next;
                self.next = sum;
                Some(current_val)
            }
            None => None, // Защита от переполнения u64
        }
    }
}

fn main() {
    println!("=== Rust Функциональное Программирование ===\n");

    // Тест Задания 1
    let products = vec![
        Product { name: "Laptop".into(), price: 1200.0, available: true },
        Product { name: "Mouse".into(), price: 25.0, available: true },
        Product { name: "Monitor".into(), price: 300.0, available: false },
        Product { name: "Keyboard".into(), price: 80.0, available: true },
    ];
    
    let (avg, avail, expensive) = analyze_products(&products);
    println!("1. Анализ продуктов:");
    println!("   Средняя цена: {:.2}", avg);
    println!("   Доступно товаров: {}", avail);
    println!("   Дорогие товары: {:?}\n", expensive.iter().map(|p| &p.name).collect::<Vec<_>>());

    // Тест Задания 2
    let orders = vec![
        Order { id: 1, amount: 150.0 },
        Order { id: 2, amount: -10.0 }, // Ошибка здесь
        Order { id: 3, amount: 50.0 },
    ];
    
    println!("2. Валидация заказов:");
    match validate_orders(&orders) {
        Ok(valid) => println!("   Все заказы валидны: {:?}", valid),
        Err(e) => println!("   Ошибка валидации: {:?}\n", e),
    }

    // Тест Задания 3
    println!("3. Итератор Фибоначчи (первые 10 чисел):");
    let fib: Vec<u64> = Fibonacci::new().take(10).collect();
    println!("   Последовательность: {:?}\n", fib);
}