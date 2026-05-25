use shop_mongo;

db.orders.createIndex({ "user_id": 1 });