package utils

import (
    "context"
    "time"
)

func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
    out := make(chan int)
    
    for _, ch := range chs {
        go func(c <-chan int) {
            defer close(out)
            for {
                select {
                case val, ok := <-c:
                    if !ok {
                        return
                    }
                    select {
                    case out <- val:
                    case <-ctx.Done():
                        return
                    }
                case <-ctx.Done():
                    return
                }
            }
        }(ch)
    }
    
    return out
}

func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
    output := make(chan int, bufferSize)
    
    go func() {
        defer close(output)
        for val := range input {
            output <- val * 2 // Простая обработка
        }
    }()
    
    return output
}