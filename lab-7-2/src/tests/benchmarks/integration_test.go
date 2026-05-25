package integration

import (
    "context"
    "net/http"
    "sync"
    "testing"
    "time"
    
    "lab-async-go/internal/server"
    "lab-async-go/internal/worker"
)

func TestIntegration_WorkerPoolWithHTTPServer(t *testing.T) {
    // Запускаем сервер
    srv := server.NewServer(":8081")
    go srv.Start()
    defer srv.Stop(context.Background())
    
    time.Sleep(100 * time.Millisecond) // Даем время серверу запуститься
    
    // Создаем worker pool
    pool := worker.NewWorkerPool(5)
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    
    tasks := []worker.Task{
        {ID: 1, Data: "http://localhost:8081/health"},
        {ID: 2, Data: "http://localhost:8081/stats"},
    }
    
    processor := func(task worker.Task) worker.Result {
        resp, err := http.Get(task.Data.(string))
        if err != nil {
            return worker.Result{TaskID: task.ID, Error: err}
        }
        defer resp.Body.Close()
        
        return worker.Result{
            TaskID: task.ID,
            Output: resp.StatusCode,
        }
    }
    
    results := pool.ProcessTasks(ctx, tasks, processor)
    
    for _, result := range results {
        if result.Error != nil {
            t.Errorf("Task %d failed: %v", result.TaskID, result.Error)
        }
        if result.Output != http.StatusOK {
            t.Errorf("Task %d expected status 200, got %v", result.TaskID, result.Output)
        }
    }
}

func TestIntegration_LoadTest(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping load test in short mode")
    }
    
    srv := server.NewServer(":8082")
    go srv.Start()
    defer srv.Stop(context.Background())
    
    time.Sleep(200 * time.Millisecond)
    
    clients := 50
    requestsPerClient := 20
    var wg sync.WaitGroup
    
    for i := 0; i < clients; i++ {
        wg.Add(1)
        go func(clientID int) {
            defer wg.Done()
            for j := 0; j < requestsPerClient; j++ {
                resp, err := http.Get("http://localhost:8082/")
                if err != nil {
                    t.Logf("Client %d request failed: %v", clientID, err)
                    continue
                }
                resp.Body.Close()
                time.Sleep(10 * time.Millisecond)
            }
        }(i)
    }
    
    wg.Wait()
    
    totalRequests := clients * requestsPerClient
    if srv.GetRequestCount() != int64(totalRequests) {
        t.Errorf("Expected %d requests, got %d", totalRequests, srv.GetRequestCount())
    }
}