from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uvicorn
from datetime import date, timedelta
from database import engine, Base 
from fastapi.middleware.cors import CORSMiddleware
import os

from models import BookCreate, BookResponse, BookUpdate, BorrowRequest, BookDetailResponse, Genre
from routers import router as books_router

app = FastAPI(
    title="Book Library API",
    description="API для управления библиотекой книг",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS для доступа с разных доменов
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "https://portfolio-site.vercel.app").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутер
app.include_router(books_router, prefix="/api/v1", tags=["books"])

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Добро пожаловать в API библиотеки книг!",
        "docs": "/docs",
        "version": "1.0.0"
    }

app.on_event("startup")
async def startup():
    # Base.metadata.create_all(bind=engine)
    print("Database tables created")

@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy", "timestamp": date.today().isoformat()}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,  # Вместо 8000
        reload=True,
        log_level="info"
    )