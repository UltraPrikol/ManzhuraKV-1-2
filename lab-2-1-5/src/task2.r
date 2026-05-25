###############################################
# ЗАДАНИЕ 2 — Отличия и примеры функций map_*
# (всё в одном коде, с комментариями)
###############################################

library(purrr)
library(datasets)
library(dplyr)

# 1. map() — базовая функция: возвращает список

# Умножаем элементы на 2
result_map <- map(1:5, ~ .x * 2)
cat("map():\n")
print(result_map)
cat("\n")


# 2. map_lgl() — логический вектор

# Проверяем, какие числа > 3
result_lgl <- map_lgl(1:5, ~ .x > 3)
cat("map_lgl():\n")
print(result_lgl)
cat("\n")


# 3. map_int() — целочисленный вектор

result_int <- map_int(1:5, ~ .x^2)
cat("map_int():\n")
print(result_int)
cat("\n")


# 4. map_dbl() — вектор чисел double

result_dbl <- map_dbl(1:3, sqrt)
cat("map_dbl():\n")
print(result_dbl)
cat("\n")


# 5. map_chr() — текстовый вектор

# Выведем типы переменных датафрейма mtcars
result_chr <- map_chr(mtcars, typeof)
cat("map_chr():\n")
print(result_chr)
cat("\n")


# 6. map_df() — возврат в виде таблицы (data.frame)

# Собираем три маленьких таблицы в одну
result_df <- map_df(1:3, ~ data.frame(x = .x, square = .x^2))
cat("map_df():\n")
print(result_df)
cat("\n")


# 7. map2() — принимает два списка и применяет функцию попарно

vec1 <- 1:3
vec2 <- c(10, 20, 30)

result_map2 <- map2_dbl(vec1, vec2, ~ .x + .y)

cat("map2():\n")
print(result_map2)
cat("\n")


# 8. pmap() — принимает список аргументов (много списков)

params <- list(
  a = 1:3,
  b = 4:6,
  c = 7:9
)

# Складываем три значения
result_pmap <- pmap_dbl(params, ~ ..1 + ..2 + ..3)

cat("pmap():\n")
print(result_pmap)
cat("\n")


# 9. imap() — как map(), но дополнительно передает имя/индекс

letters_vec <- letters[1:4]

# Выводим: индекс и значение
result_imap <- imap_chr(letters_vec, ~ paste("index:", .y, "| value:", .x))

cat("imap():\n")
print(result_imap)
cat("\n")


# 10. walk() — для побочных эффектов (ничего не возвращает)

cat("walk(): вывод элементов:\n")
walk(1:3, ~ print(.x))  # просто печатает
cat("\n")


# ИТОГОВАЯ СПРАВКА

cat("-------------------------------------------------------------\n")
cat("КРАТКОЕ ОПИСАНИЕ ФУНКЦИЙ map_*:\n")
cat("map()      — список\n")
cat("map_lgl()  — логический вектор\n")
cat("map_int()  — целочисленный вектор\n")
cat("map_dbl()  — double вектор\n")
cat("map_chr()  — строковый вектор\n")
cat("map_df()   — результат как data.frame\n")
cat("map2()     — два входных списка\n")
cat("pmap()     — много списков\n")
cat("imap()     — значение + имя/индекс\n")
cat("walk()     — только побочные эффекты, ничего не возвращает\n")
cat("-------------------------------------------------------------\n")
