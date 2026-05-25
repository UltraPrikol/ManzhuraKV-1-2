get_negative_values <- function(df) {
  result <- list()
  
  for (name in names(df)) {
    negatives <- df[[name]][df[[name]] < 0]
    
    if (length(negatives) > 0) {
      result[[name]] <- negatives
    }
  }
  
  if (length(result) == 0) {
    cat("В данных нет переменных с отрицательными значениями.\n")
  } else {
    cat("Найдены отрицательные значения:\n")
    print(result)
  }
  
  return(result)
}

# Пример данных
df <- data.frame(
  a = c(1, -2, 3, -4),
  b = c(5, 6, 7, 8),
  c = c(-1, -3, -5, -7)
)

# Вызов функции с выводом
get_negative_values(df)
