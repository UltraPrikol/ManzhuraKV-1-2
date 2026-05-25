library(purrr)
library(repurrrsive)

# исходный список
sw_films

# 1. Извлекаем названия фильмов
film_names <- map_chr(sw_films, "title")

# 2. Создаём новый именованный список, аналогичный исходному
my_films <- sw_films |> 
  set_names(film_names)

# 3. Проверка
names(my_films)
my_films[["A New Hope"]]  # доступ по имени
my_films[[1]]             # доступ по индексу
