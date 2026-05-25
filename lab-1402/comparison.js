use shop_mongo;

print("--- TOP 3 Users by Spending ---");
var topUsers = db.orders.aggregate([
    { $unwind: "$items" },
    {
        $group: {
            _id: "$user_id",
            total_spent: { $sum: { $multiply: ["$items.quantity", "$items.price"] } }
        }
    },
    { $sort: { total_spent: -1 } },
    { $limit: 3 },
    {
        $lookup: {
            from: "users",
            localField: "_id",
            foreignField: "_id",
            as: "user"
        }
    },
    { $unwind: "$user" },
    {
        $project: {
            full_name: "$user.full_name",
            total_spent: 1
        }
    }
]).toArray();
printjson(topUsers);

print("--- Orders with Total Amounts (JOIN Users) ---");
var ordersJoin = db.orders.aggregate([
    {
        $lookup: {
            from: "users",
            localField: "user_id",
            foreignField: "_id",
            as: "user_info"
        }
    },
    { $unwind: "$user_info" },
    {
        $addFields: {
            total_amount: {
                $sum: {
                    $map: {
                        input: "$items",
                        as: "item",
                        in: { $multiply: ["$$item.quantity", "$$item.price"] }
                    }
                }
            }
        }
    },
    {
        $project: {
            _id: 1,
            order_date: 1,
            status: 1,
            "user_info.full_name": 1,
            "user_info.email": 1,
            total_amount: 1
        }
    }
]).toArray();
printjson(ordersJoin);