package main

import (
    "fmt"
    "log"
    "net/http"
    "sync"
    "time"
)

func main() {
    fmt.Println("=== Лабораторная работа: Асинхронное программирование в Go ===")
    
    // Демонстрация всех паттернов
    var wg sync.WaitGroup
    
    // 1. Базовые горутины
    wg.Add(1)
    go func() {
        defer wg.Done()
        fmt.Println("\n1. Базовые горутины:")
        demoBasicGoroutines()
    }()
    
    // 2. Worker Pool
    wg.Add(1)
    go func() {
        defer wg.Done()
        fmt.Println("\n2. Worker Pool:")
        demoWorkerPool()
    }()
    
    wg.Wait()
    
    // 3. HTTP сервер
    fmt.Println("\n3. HTTP Сервер:")
    fmt.Println("Запуск сервера на http://localhost:8080")
    fmt.Println("Для тестирования выполните: ab -n 1000 -c 100 http://localhost:8080/")
    
    go startHTTPServer()
    
    // Ожидание завершения
    select {
    case <-time.After(30 * time.Second):
        fmt.Println("Демонстрация завершена")
    }
}

func demoBasicGoroutines() {
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Горутина %d работает\n", id)
            time.Sleep(time.Second)
        }(i)
    }
    wg.Wait()
}

func demoWorkerPool() {
    tasks := make(chan int, 5)
    var wg sync.WaitGroup
    
    // Воркеры
    for i := 0; i < 2; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for task := range tasks {
                fmt.Printf("Воркер %d обработал задачу %d\n", workerID, task)
                time.Sleep(500 * time.Millisecond)
            }
        }(i)
    }
    
    // Задачи
    for i := 0; i < 5; i++ {
        tasks <- i
    }
    close(tasks)
    
    wg.Wait()
}

func startHTTPServer() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Время: %s", time.Now().Format("15:04:05"))
    })
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}