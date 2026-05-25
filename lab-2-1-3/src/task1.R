# --- Создаём дженерик ---
area <- function(x, ...) {
  UseMethod("area")
}

# --- Метод по умолчанию ---
area.default <- function(x, ...) {
  stop("Невозможно обработать переданный объект: отсутствует метод для данного класса.")
}

# ===== КЛАССЫ ФИГУР =====

# --- Круг ---
circle <- function(r) {
  structure(list(r = r), class = "circle")
}

area.circle <- function(x, ...) {
  pi * x$r^2
}

# --- Прямоугольник ---
rectangle <- function(a, b) {
  structure(list(a = a, b = b), class = "rectangle")
}

area.rectangle <- function(x, ...) {
  x$a * x$b
}

# --- Треугольник ---
triangle <- function(a, h) {
  structure(list(a = a, h = h), class = "triangle")
}

area.triangle <- function(x, ...) {
  x$a * x$h / 2
}

# ===== ПРОВЕРКА =====
c1 <- circle(5)
area(c1)

r1 <- rectangle(4, 6)
area(r1)

t1 <- triangle(10, 8)
area(t1)

area(123)      # вызовет area.default — ошибка
