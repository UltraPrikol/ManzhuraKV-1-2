classes <- numeric(7)

cat("Введите количество занятий по каждому дню недели:\n")

for (i in 1:7) {
  classes[i] <- as.numeric(readline(paste("День", i, ": ")))
}

average <- mean(classes)

rounded_average <- round(average)

cat("Среднее количество занятий в неделю:", rounded_average, "\n")
