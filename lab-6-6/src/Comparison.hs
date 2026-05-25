module Comparison where

-- Модель данных
data User = User { userId :: Int, userName :: String, userEmail :: String }
data Product = Product { productId :: Int, productName :: String, productPrice :: Double, productCategory :: String }
data OrderItem = OrderItem { itemProduct :: Product, itemQuantity :: Int }
data Order = Order { orderId :: Int, orderUser :: User, orderItems :: [OrderItem], orderStatus :: String }

-- Пример данных
users :: [User]
users = [
    User 1 "John Doe" "john@example.com",
    User 2 "Jane Smith" "jane@example.com"
    ]

products :: [Product]
products = [
    Product 1 "iPhone" 999.99 "electronics",
    Product 2 "MacBook" 1999.99 "electronics",
    Product 3 "T-shirt" 29.99 "clothing"
    ]

orders :: [Order]
orders = [
    Order 1 (users !! 0) [OrderItem (products !! 0) 1, OrderItem (products !! 2) 2] "completed",
    Order 2 (users !! 1) [OrderItem (products !! 1) 1] "pending"
    ]

-- Функции обработки
calculateOrderTotal :: Order -> Double
calculateOrderTotal order = sum [productPrice (itemProduct item) * fromIntegral (itemQuantity item) | item <- orderItems order]

filterOrdersByStatus :: [Order] -> String -> [Order]
filterOrdersByStatus orders status = filter (\order -> orderStatus order == status) orders

getTopExpensiveOrders :: [Order] -> Int -> [Order]
getTopExpensiveOrders orders n = take n $ sortBy (\a b -> compare (calculateOrderTotal b) (calculateOrderTotal a)) orders

applyDiscount :: Order -> Double -> Order
applyDiscount order discount = order { orderItems = map (applyItemDiscount discount) (orderItems order) }
  where
    applyItemDiscount discount item = item { itemProduct = (itemProduct item) { productPrice = productPrice (itemProduct item) * (1 - discount) } }

-- Основная функция
main :: IO ()
main = do
    let completedOrders = filterOrdersByStatus orders "completed"
    let totalRevenue = sum $ map calculateOrderTotal completedOrders
    putStrLn $ "Общая выручка: " ++ show totalRevenue
    putStrLn $ "Топ заказы: " ++ show (map (calculateOrderTotal . fst) (zip (getTopExpensiveOrders orders 2) [1..]))