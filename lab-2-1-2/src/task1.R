show_solution <- function(shape, params, area) {
  cat("\nХод решения:\n")

  if (shape == "circle") {
    cat("Фигура: круг\n")
    cat("Формула площади: S = π * r^2\n")
    cat("r =", params$r, "\n")
    cat("S = pi *", params$r, "^ 2 =", area, "\n")
  }

  if (shape == "square") {
    cat("Фигура: квадрат\n")
    cat("Формула площади: S = a^2\n")
    cat("a =", params$a, "\n")
    cat("S =", params$a, "^ 2 =", area, "\n")
  }

  if (shape == "rectangle") {
    cat("Фигура: прямоугольник\n")
    cat("Формула площади: S = a * b\n")
    cat("a =", params$a, ", b =", params$b, "\n")
    cat("S =", params$a, "*", params$b, "=", area, "\n")
  }

  if (shape == "triangle") {
    cat("Фигура: треугольник\n")
    cat("Формула площади: S = (a * h) / 2\n")
    cat("a =", params$a, ", h =", params$h, "\n")
    cat("S = (", params$a, "*", params$h, ")/2 =", area, "\n")
  }

  cat("\nПлощадь фигуры =", area, "\n")
}

valid_shapes <- c("circle", "square", "rectangle", "triangle")
attempts <- 0

repeat {
  shape <- tolower(readline("Введите название фигуры (circle, square, rectangle, triangle): "))

  if (shape %in% valid_shapes) {
    break
  } else {
    attempts <- attempts + 1
    cat("Ошибка: такой фигуры нет. Попытка", attempts, "из 3.\n")

    if (attempts >= 3) {
      cat("Вы 3 раза ввели некорректные данные. Программа завершена.\n")
      stop()
    }
  }
}

if (shape == "circle") {
  r <- as.numeric(readline("Введите радиус r: "))
  area <- pi * r^2
  params <- list(r = r)
}

if (shape == "square") {
  a <- as.numeric(readline("Введите сторону a: "))
  area <- a^2
  params <- list(a = a)
}

if (shape == "rectangle") {
  a <- as.numeric(readline("Введите сторону a: "))
  b <- as.numeric(readline("Введите сторону b: "))
  area <- a * b
  params <- list(a = a, b = b)
}

if (shape == "triangle") {
  a <- as.numeric(readline("Введите основание a: "))
  h <- as.numeric(readline("Введите высоту h: "))
  area <- (a * h) / 2
  params <- list(a = a, h = h)
}

cat("\nРезультат:\n")
cat("Площадь =", area, "\n")

show_solution(shape, params, area)
