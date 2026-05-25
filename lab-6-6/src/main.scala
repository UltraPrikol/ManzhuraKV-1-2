import scala.util.Try

case class Product(price: Double)
case class Item(product: Product, quantity: Int)
case class Order(items: List[Item])

object Main extends App {
  def safeCalculateTotal(order: Order): Option[Double] = {
    Try {
      order.items.map(item => item.product.price * item.quantity).sum
    }.toOption
  }

  val order = Order(List(Item(Product(100.0), 2), Item(Product(50.0), 1)))
  
  safeCalculateTotal(order) match {
    case Some(total) => println(s"Scala: Расчет завершен: $total")
    case None        => println("Scala: Ошибка при расчете")
  }
}