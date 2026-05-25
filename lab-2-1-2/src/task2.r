polygon_area <- function(x, y) {
  n <- length(x)
  sum1 <- 0
  sum2 <- 0
  
  for (i in 1:(n - 1)) {
    sum1 <- sum1 + x[i] * y[i + 1]
    sum2 <- sum2 + y[i] * x[i + 1]
  }
  
  sum1 <- sum1 + x[n] * y[1]
  sum2 <- sum2 + y[n] * x[1]
  
  area <- abs(sum1 - sum2) / 2
  return(area)
}


N <- as.numeric(readline("Введите количество вершин многоугольника N: "))

x <- numeric(N)
y <- numeric(N)

cat("Введите координаты вершин (x y) по одной вершине на строку:\n")

for (i in 1:N) {
  coords <- strsplit(readline(paste("Вершина", i, ": ")), " ")[[1]]
  x[i] <- as.numeric(coords[1])
  y[i] <- as.numeric(coords[2])
}

result <- polygon_area(x, y)

cat("\nПлощадь многоугольника =", result, "\n")
