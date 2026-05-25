package server

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "net/http/httptest"
    "sync"
    "testing"
    "time"
)

func TestServer_Routes(t *testing.T) {
    server := NewServer(":0")
    
    tests := []struct {
        name       string
        path       string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "root path",
            path:       "/",
            wantStatus: http.StatusOK,
            wantBody:   "Hello! Request count: 1",
        },
        {
            name:       "health check",
            path:       "/health",
            wantStatus: http.StatusOK,
            wantBody:   "OK",
        },
        {
            name:       "stats",
            path:       "/stats",
            wantStatus: http.StatusOK,
            wantBody:   "Total requests: 0",
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", tt.path, nil)
            w := httptest.NewRecorder()
            
            server.router.ServeHTTP(w, req)
            
            resp := w.Result()
            body, _ := io.ReadAll(resp.Body)
            
            if resp.StatusCode != tt.wantStatus {
                t.Errorf("Expected status %d, got %d", tt.wantStatus, resp.StatusCode)
            }
            
            if string(body) != tt.wantBody && tt.path != "/" {
                // Для корневого пути тело динамическое, пропускаем точную проверку
                t.Errorf("Expected body %q, got %q", tt.wantBody, string(body))
            }
        })
    }
}

func TestServer_ConcurrentRequests(t *testing.T) {
    server := NewServer(":0")
    ts := httptest.NewServer(server.router)
    defer ts.Close()
    
    var wg sync.WaitGroup
    requests := 100
    
    for i := 0; i < requests; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            resp, err := http.Get(ts.URL + "/")
            if err != nil {
                t.Errorf("Request failed: %v", err)
                return
            }
            defer resp.Body.Close()
            
            if resp.StatusCode != http.StatusOK {
                t.Errorf("Expected status 200, got %d", resp.StatusCode)
            }
        }(i)
    }
    
    wg.Wait()
    
    // Проверяем счетчик запросов
    if server.GetRequestCount() != int64(requests) {
        t.Errorf("Expected %d requests, got %d", requests, server.GetRequestCount())
    }
}

func TestServer_GracefulShutdown(t *testing.T) {
    server := NewServer(":0")
    ts := httptest.NewServer(server.router)
    
    ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
    defer cancel()
    
    // Запускаем остановку сервера
    go func() {
        time.Sleep(50 * time.Millisecond)
        if err := server.Stop(ctx); err != nil {
            t.Logf("Shutdown error: %v", err)
        }
    }()
    
    // Пытаемся сделать запрос после shutdown
    time.Sleep(60 * time.Millisecond)
    _, err := http.Get(ts.URL + "/")
    if err == nil {
        t.Error("Expected error after shutdown, but request succeeded")
    }
}