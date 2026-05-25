# Установка и загрузка необходимых пакетов
install.packages("janeaustenr")
install.packages("stringr")
install.packages("dplyr")

library(janeaustenr)
library(stringr)
library(dplyr)

# ------------------ ФУНКЦИИ ИЗ ЗАДАНИЯ ------------------

extract_words <- function(book_name) {
  text <- subset(austen_books(), book == book_name)$text
  str_extract_all(text, boundary("word")) %>% unlist %>% tolower()
}

janeausten_words <- function() {
  books <- austen_books()$book %>% unique() %>% as.character()
  words <- sapply(books, extract_words) %>% unlist()
  words
}

select_words <- function(letter, words, min_length = 1) {
  min_length_words <- words[nchar(words) >= min_length]
  grep(paste0("^", letter), min_length_words, value = TRUE)
}

max_frequency <- function(letter, words, min_length = 1) {
  w <- select_words(letter, words = words, min_length = min_length)
  frequency <- table(w)
  # если нет слов на эту букву — вернуть NA
  if (length(frequency) == 0) return(NA)
  frequency[which.max(frequency)]
}


# 1. Создаем вектор всех слов
words <- janeausten_words()

# 2. Получаем именованный вектор максимальных частот
result <- sapply(letters, max_frequency, words = words, min_length = 5)

# 3. Визуализация
barplot(result,
        las = 2,
        main = "Наиболее часто встречающиеся слова по буквам алфавита\n(длина ≥ 5)",
        col = "lightblue",
        ylab = "Частота")

