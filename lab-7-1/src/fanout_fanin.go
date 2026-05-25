package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func producer(ctx context.Context, id int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for i := 0; i < 5; i++ {
            select {
            case out <- i:
                fmt.Printf("Producer %d: %d\n", id, i)
            case <-ctx.Done():
                fmt.Printf("Producer %d cancelled\n", id)
                return
            }
            time.Sleep(200 * time.Millisecond)
        }
    }()
    return out
}

func worker(ctx context.Context, in <-chan int, id int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
                fmt.Printf("Worker %d processed %d\n", id, n)
            case <-ctx.Done():
                fmt.Printf("Worker %d cancelled\n", id)
                return
            }
        }
    }()
    return out
}

func merge(ctx context.Context, inputs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)
    
    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }
    
    wg.Add(len(inputs))
    for _, input := range inputs {
        go output(input)
    }
    
    go func() {
        wg.Wait()
        close(out)
    }()
    
    return out
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancel()
    
    // Fan-out: несколько продюсеров
    p1 := producer(ctx, 1)
    p2 := producer(ctx, 2)
    
    // Worker pool
    w1 := worker(ctx, p1, 1)
    w2 := worker(ctx, p2, 2)
    
    // Fan-in: объединение результатов
    results := merge(ctx, w1, w2)
    
    for result := range results {
        fmt.Printf("Result: %d\n", result)
    }
    
    fmt.Println("Processing completed")
}