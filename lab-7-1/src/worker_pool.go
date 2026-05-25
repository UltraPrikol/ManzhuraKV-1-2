package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
)

type Task struct {
    ID int
}

type Result struct {
    TaskID int
    Output string
}

func worker(id int, tasks <-chan Task, results chan<- Result, wg *sync.WaitGroup) {
    defer wg.Done()
    for task := range tasks {
        fmt.Printf("Worker %d processing task %d\n", id, task.ID)
        time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
        results <- Result{
            TaskID: task.ID,
            Output: fmt.Sprintf("Task %d completed by worker %d", task.ID, id),
        }
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    
    numWorkers := 3
    numTasks := 10
    
    tasks := make(chan Task, numTasks)
    results := make(chan Result, numTasks)
    
    var wg sync.WaitGroup
    
    // Запуск воркеров
    for i := 1; i <= numWorkers; i++ {
        wg.Add(1)
        go worker(i, tasks, results, &wg)
    }
    
    // Отправка задач
    for i := 1; i <= numTasks; i++ {
        tasks <- Task{ID: i}
    }
    close(tasks)
    
    // Закрытие results после завершения всех воркеров
    go func() {
        wg.Wait()
        close(results)
    }()
    
    // Обработка результатов
    for result := range results {
        fmt.Printf("Result: %s\n", result.Output)
    }
    
    fmt.Println("All tasks completed")
}