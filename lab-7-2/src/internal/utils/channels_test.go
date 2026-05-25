package utils

import (
    "context"
    "testing"
    "time"
)

func TestMergeChannels(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    
    ch1 := make(chan int)
    ch2 := make(chan int)
    
    go func() {
        defer close(ch1)
        for i := 0; i < 3; i++ {
            ch1 <- i
        }
    }()
    
    go func() {
        defer close(ch2)
        for i := 3; i < 6; i++ {
            ch2 <- i
        }
    }()
    
    merged := MergeChannels(ctx, ch1, ch2)
    
    var results []int
    for val := range merged {
        results = append(results, val)
    }
    
    if len(results) != 6 {
        t.Errorf("Expected 6 values, got %d", len(results))
    }
}

func TestBufferedChannelProcessor(t *testing.T) {
    input := make(chan int, 5)
    
    for i := 1; i <= 5; i++ {
        input <- i
    }
    close(input)
    
    output := BufferedChannelProcessor(input, 3)
    
    expected := []int{2, 4, 6, 8, 10}
    var results []int
    
    for val := range output {
        results = append(results, val)
    }
    
    if len(results) != len(expected) {
        t.Errorf("Expected %d results, got %d", len(expected), len(results))
    }
    
    for i, val := range results {
        if val != expected[i] {
            t.Errorf("Expected %d at position %d, got %d", expected[i], i, val)
        }
    }
}

func TestChannelTimeout(t *testing.T) {
    ch := make(chan int)
    
    select {
    case <-ch:
        t.Error("Should not receive from channel")
    case <-time.After(100 * time.Millisecond):
        // Ожидаемое поведение - таймаут
    }
}