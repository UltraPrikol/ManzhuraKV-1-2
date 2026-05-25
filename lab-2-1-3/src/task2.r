# ===== КЛАСС МИКРОВОЛНОВКА =====

microwave <- function(power = 800, door = "closed") {
  structure(list(
    power = power,
    door = door
  ), class = "microwave")
}

# --- Метод открыть дверь ---
open_door <- function(mw) {
  mw$door <- "open"
  cat("Дверь микроволновки открыта\n")
  return(mw)
}

# --- Метод закрыть дверь ---
close_door <- function(mw) {
  mw$door <- "closed"
  cat("Дверь микроволновки закрыта\n")
  return(mw)
}

# --- Метод приготовления пищи ---
cook <- function(mw, time_sec) {
  if (mw$door == "open") {
    stop("Нельзя готовить: дверь открыта!")
  }
  cat("Приготовление пищи... Ожидайте.\n")

  # Время готовки уменьшаем пропорционально мощности
  wait_time <- time_sec * (800 / mw$power)

  Sys.sleep(wait_time)
  cat("Пища готова!\n")
}

# Объект по умолчанию
mw1 <- microwave()

# Объект со своими значениями
mw2 <- microwave(power = 1200, door = "open")

# --- Демонстрация работы ---

mw1 <- open_door(mw1)
mw1 <- close_door(mw1)
cook(mw1, 3)

mw2 <- close_door(mw2)
cook(mw2, 3)
