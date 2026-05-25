package main

import (
    "fmt"
    "time"
)

func producer(ch chan<- int) {
    for i := 0; i < 10; i++ {
        ch <- i
        fmt.Printf("Produced: %d\n", i)
    }
    close(ch)
}

func consumer(ch <-chan int) {
    for {
        select {
        case val, ok := <-ch:
            if !ok {
                fmt.Println("Channel closed")
                return
            }
            fmt.Printf("Consumed: %d\n", val)
            time.Sleep(500 * time.Millisecond)
        case <-time.After(2 * time.Second):
            fmt.Println("Timeout occurred")
            return
        }
    }
}

func main() {
    ch := make(chan int, 3)
    go producer(ch)
    consumer(ch)
}