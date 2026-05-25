use shop_mongo;

print("--- READ: Orders for Alice ---");
var aliceOrders = db.orders.aggregate([
    {
        $lookup: {
            from: "users",
            localField: "user_id",
            foreignField: "_id",
            as: "user_info"
        }
    },
    { $unwind: "$user_info" },
    { $match: { "user_info.email": "alice@example.com" } },
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
    }
]).toArray();
printjson(aliceOrders);

print("--- UPDATE: Adding discounts for expensive orders ---");
db.orders.find().forEach(function(order) {
    var total = order.items.reduce(function(sum, item) {
        return sum + (item.quantity * item.price);
    }, 0);
    if (total > 80000) {
        db.orders.updateOne({ _id: order._id }, { $set: { discount: 10 } });
    }
});

print("--- DELETE: Removing old cancelled orders ---");
const boundaryDate = new Date();
boundaryDate.setDate(boundaryDate.getDate() - 30);
db.orders.deleteMany({
    status: "cancelled",
    order_date: { $lt: boundaryDate }
});

print("--- AGGREGATION: Revenue by Category ---");
var categoryReport = db.orders.aggregate([
    { $unwind: "$items" },
    {
        $lookup: {
            from: "products",
            localField: "items.product_id",
            foreignField: "_id",
            as: "product_info"
        }
    },
    { $unwind: "$product_info" },
    {
        $group: {
            _id: "$product_info.category",
            total_quantity: { $sum: "$items.quantity" },
            total_revenue: { $sum: { $multiply: ["$items.quantity", "$items.price"] } },
            avg_price: { $avg: "$items.price" }
        }
    },
    { $sort: { total_revenue: -1 } },
    {
        $project: {
            category: "$_id",
            _id: 0,
            total_quantity: 1,
            total_revenue: 1,
            avg_price: 1
        }
    }
]).toArray();
printjson(categoryReport);