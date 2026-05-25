package benchmarks

import (
    "context"
    "sync"
    "testing"
    "time"
    
    "lab-async-go/internal/utils"
    "lab-async-go/internal/worker"
)

func BenchmarkCounter_Increment(b *testing.B) {
    counter := &utils.Counter{}
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            counter.Increment()
        }
    })
}

func BenchmarkWorkerPool_ProcessTasks(b *testing.B) {
    pool := worker.NewWorkerPool(10)
    ctx := context.Background()
    
    processor := func(task worker.Task) worker.Result {
        time.Sleep(1 * time.Millisecond)
        return worker.Result{
            TaskID: task.ID,
            Output: task.Data.(int) * 2,
        }
    }
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        tasks := make([]worker.Task, 100)
        for j := 0; j < 100; j++ {
            tasks[j] = worker.Task{ID: j, Data: j}
        }
        pool.ProcessTasks(ctx, tasks, processor)
    }
}

func BenchmarkGoroutineCreation(b *testing.B) {
    var wg sync.WaitGroup
    worker := func() {
        defer wg.Done()
        // Легкая работа
        time.Sleep(1 * time.Microsecond)
    }
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        wg.Add(1)
        go worker()
    }
    wg.Wait()
}

func BenchmarkChannelCommunication(b *testing.B) {
    ch := make(chan int, b.N)
    
    // Горутина для чтения
    go func() {
        for range ch {
        }
    }()
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ch <- i
    }
    close(ch)
}