import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

// --- Модели данных ---
case class SalesRecord(item: String, category: String, amount: Double)
case class Order(id: Int, userId: Int, amount: Double)

object SalesApp {

  def main(args: Array[String]): Unit = {
    println("=== Scala FP Lab: Результаты выполнения ===\n")

    // --- Тест Задания 1: Анализ продаж ---
    val sales = List(
      SalesRecord("Laptop", "Tech", 1000.0),
      SalesRecord("Phone", "Tech", 500.0),
      SalesRecord("Apple", "Food", 2.0),
      SalesRecord("Bread", "Food", 1.5)
    )
    val analysis = analyzeSales(sales)
    println(s"1. Анализ продаж (Категория -> Сумма, Кол-во):")
    analysis.foreach { case (cat, (sum, count)) => println(s"   $cat: Сумма = $sum, Кол-во = $count") }


    // --- Тест Задания 2: Цепочка обработки заказа ---
    println("\n2. Обработка заказов (Either Pipeline):")
    val orders = List(
      Order(1, 101, 1200.0), // Успешный
      Order(2, -1, 500.0),   // Ошибка пользователя
      Order(3, 102, -50.0)   // Ошибка платежа
    )
    
    orders.foreach { order =>
      val result = processOrderPipeline(order)
      println(s"   Заказ #${order.id}: $result")
    }


    // --- Тест Задания 3: Spark Job ---
    println("\n3. Spark Report (Вывод в консоль):")
    // Инициализация Spark (в локальном режиме)
    val spark = SparkSession.builder()
      .appName("SalesReport")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    val rawData = Seq(
      ("2023-10-01", "Laptop", "Tech", 1000.0, 1),
      ("2023-10-01", "Phone", "Tech", 500.0, 2),
      ("2023-10-02", "Apple", "Food", 2.0, 10)
    ).toDF("date", "item", "category", "price", "quantity")

    val report = createSalesReport(rawData)
    report.show()

    spark.stop()
  }

  // --- Задание 1: Анализ продаж ---
  def analyzeSales(sales: List[SalesRecord]): Map[String, (Double, Int)] = {
    // Используем groupBy по категории, затем трансформируем значения
    sales.groupBy(_.category).view.mapValues { records =>
      val totalSum = records.map(_.amount).sum
      val count = records.size
      (totalSum, count)
    }.toMap
  }

  // --- Задание 2: Обработка ошибок через Either ---
  def processOrderPipeline(order: Order): Either[String, Double] = {
    
    def validateUser(o: Order): Either[String, Order] =
      if (o.userId > 0) Right(o) else Left("Invalid User ID")

    def validatePayment(o: Order): Either[String, Order] =
      if (o.amount > 0) Right(o) else Left("Payment amount must be positive")

    def calculateDiscount(o: Order): Either[String, Double] = {
      val discount = if (o.amount > 1000) 0.1 else 0.05
      Right(o.amount * (1 - discount))
    }

    // Цепочка операций
    for {
      userValid    <- validateUser(order)
      paymentValid <- validatePayment(userValid)
      finalAmount  <- calculateDiscount(paymentValid)
    } yield finalAmount
  }

  // --- Задание 3: Spark Аналитика ---
  def createSalesReport(df: DataFrame): DataFrame = {
    df.withColumn("revenue", col("price") * col("quantity"))
      .groupBy("date", "category")
      .agg(
        sum("revenue").as("total_revenue"),
        count("item").as("distinct_items"),
        avg("price").as("avg_price")
      )
      .orderBy("date")
  }
}