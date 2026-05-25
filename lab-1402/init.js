use shop_mongo;

db.users.insertMany([
    {
        _id: 1,
        email: "alice@example.com",
        full_name: "Alice Smith",
        created_at: new Date(),
        address: {
            city: "Moscow",
            street: "Tverskaya",
            zipcode: "101000"
        }
    },
    {
        _id: 2,
        email: "bob@example.com", 
        full_name: "Bob Johnson",
        created_at: new Date(),
        address: {
            city: "Saint Petersburg",
            street: "Nevsky",
            zipcode: "191186"
        }
    },
    {
        _id: 3,
        email: "charlie@example.com",
        full_name: "Charlie Brown",
        created_at: new Date(),
        address: {
            city: "Kazan",
            street: "Baumana",
            zipcode: "420000"
        }
    }
]);

db.products.insertMany([
    {
        _id: 1,
        name: "Ноутбук",
        category: "Электроника",
        price: 75000,
        stock_quantity: 10,
        specs: {
            brand: "Lenovo",
            ram: "16GB",
            storage: "512GB SSD"
        }
    },
    {
        _id: 2,
        name: "Мышь",
        category: "Электроника",
        price: 1500,
        stock_quantity: 50
    },
    {
        _id: 3,
        name: "Книга SQL",
        category: "Книги",
        price: 2500,
        stock_quantity: 30,
        specs: {
            author: "Дмитрий К.",
            pages: 450
        }
    },
    {
        _id: 4,
        name: "Механическая клавиатура",
        category: "Электроника",
        price: 5500,
        stock_quantity: 15,
        specs: {
            switches: "Linear",
            hotswap: true
        }
    },
    {
        _id: 5,
        name: "Полимерная смола ABS-Like",
        category: "Расходные материалы",
        price: 3200,
        stock_quantity: 25,
        specs: {
            weight: "1kg",
            color: "Grey"
        }
    }
]);

db.orders.insertMany([
    {
        _id: 1,
        user_id: 1,
        order_date: new Date(),
        status: "completed",
        items: [
            { product_id: 1, quantity: 1, price: 75000 },
            { product_id: 2, quantity: 4, price: 1500 }
        ]
    },
    {
        _id: 2,
        user_id: 2,
        order_date: new Date(),
        status: "completed",
        items: [
            { product_id: 3, quantity: 1, price: 2500 },
            { product_id: 4, quantity: 1, price: 5500 }
        ]
    },
    {
        _id: 3,
        user_id: 3,
        order_date: new Date(),
        status: "pending",
        items: [
            { product_id: 4, quantity: 2, price: 5500 },
            { product_id: 5, quantity: 3, price: 3200 }
        ]
    },
    {
        _id: 4,
        user_id: 3,
        order_date: new Date(new Date().setDate(new Date().getDate() - 40)),
        status: "cancelled",
        items: [
            { product_id: 2, quantity: 1, price: 1500 },
            { product_id: 5, quantity: 1, price: 3200 }
        ]
    }
]);