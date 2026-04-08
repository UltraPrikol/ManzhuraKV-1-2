from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from datetime import date, timedelta
from collections import Counter

from models import BookCreate, BookResponse, BookUpdate, BorrowRequest, BookDetailResponse, Genre
# Имитация базы данных (теперь живет прямо в роутере, чтобы не было циклов)
books_db = {}
borrow_records = {}
current_id = 1

def get_next_id() -> int:
    global current_id
    id_ = current_id
    current_id += 1
    return id_


def book_to_response(book_id: int, book_data: dict) -> BookResponse:
    return BookResponse(
        id=book_id,
        title=book_data["title"],
        author=book_data["author"],
        genre=book_data["genre"],
        publication_year=book_data["publication_year"],
        pages=book_data["pages"],
        isbn=book_data["isbn"],
        available=book_data.get("available", True)
    )


router = APIRouter()

# GET /books - получение списка всех книг с фильтрацией
@router.get("/books", response_model=List[BookResponse])
async def get_books(
    genre: Optional[Genre] = Query(None, description="Фильтр по жанру"),
    author: Optional[str] = Query(None, description="Фильтр по автору"),
    available_only: bool = Query(False, description="Только доступные книги"),
    skip: int = Query(0, ge=0, description="Количество книг для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит книг на странице")
):
    filtered_books = []
    
    for book_id, book_data in books_db.items():
        # Фильтрация по жанру
        if genre and book_data["genre"] != genre:
            continue
            
        # Фильтрация по автору (регистронезависимая)
        if author and author.lower() not in book_data["author"].lower():
            continue
            
        # Фильтрация по доступности
        if available_only and not book_data.get("available", True):
            continue
            
        filtered_books.append(book_to_response(book_id, book_data))
    
    # Пагинация
    return filtered_books[skip : skip + limit]

# GET /books/{book_id} - получение книги по ID
@router.get("/books/{book_id}", response_model=BookDetailResponse)
async def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    
    book_data = books_db[book_id]
    response = BookDetailResponse(
        id=book_id,
        title=book_data["title"],
        author=book_data["author"],
        genre=book_data["genre"],
        publication_year=book_data["publication_year"],
        pages=book_data["pages"],
        isbn=book_data["isbn"],
        available=book_data.get("available", True)
    )
    
    # Добавляем инфу о заимствовании, если книга на руках
    if not response.available and book_id in borrow_records:
        record = borrow_records[book_id]
        response.borrowed_by = record["borrower_name"]
        response.borrowed_date = record["borrowed_date"]
        response.return_date = record["return_date"]
        
    return response

# POST /books - создание новой книги
@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    # Проверка уникальности ISBN
    for existing_book in books_db.values():
        if existing_book["isbn"] == book.isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Книга с таким ISBN уже существует"
            )
    
    book_id = get_next_id()
    book_dict = book.model_dump()
    book_dict["available"] = True  # Новая книга всегда доступна
    
    books_db[book_id] = book_dict
    return book_to_response(book_id, books_db[book_id])

# PUT /books/{book_id} - обновление книги
@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    
    current_data = books_db[book_id]
    update_data = book_update.model_dump(exclude_unset=True)
    
    # Проверка уникальности ISBN, если он обновляется
    if "isbn" in update_data:
        for ex_id, ex_book in books_db.items():
            if ex_book["isbn"] == update_data["isbn"] and ex_id != book_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Другая книга с таким ISBN уже существует"
                )
    
    current_data.update(update_data)
    books_db[book_id] = current_data
    return book_to_response(book_id, current_data)

# DELETE /books/{book_id} - удаление книги
@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    
    if not books_db[book_id].get("available", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Нельзя удалить книгу, которая находится на руках"
        )
        
    del books_db[book_id]
    if book_id in borrow_records:
        del borrow_records[book_id]
        
    return None

# POST /books/{book_id}/borrow - заимствование книги
@router.post("/books/{book_id}/borrow", response_model=BookDetailResponse)
async def borrow_book(book_id: int, borrow_request: BorrowRequest):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
        
    if not books_db[book_id].get("available", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Книга уже выдана другому читателю"
        )
        
    books_db[book_id]["available"] = False
    
    today = date.today()
    return_date = today + timedelta(days=borrow_request.return_days)
    
    borrow_records[book_id] = {
        "borrower_name": borrow_request.borrower_name,
        "borrowed_date": today,
        "return_date": return_date
    }
    
    return await get_book(book_id)

# POST /books/{book_id}/return - возврат книги
@router.post("/books/{book_id}/return", response_model=BookResponse)
async def return_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
        
    if books_db[book_id].get("available", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Книга уже находится в библиотеке (не была выдана)"
        )
        
    books_db[book_id]["available"] = True
    if book_id in borrow_records:
        del borrow_records[book_id]
        
    return book_to_response(book_id, books_db[book_id])

# GET /stats - статистика библиотеки
@router.get("/stats")
async def get_library_stats():
    total = len(books_db)
    borrowed = len(borrow_records)
    available = total - borrowed
    
    genres = Counter(book["genre"] for book in books_db.values())
    authors = Counter(book["author"] for book in books_db.values())
    
    most_prolific = authors.most_common(1)[0][0] if authors else None
    
    return {
        "total_books": total,
        "available_books": available,
        "borrowed_books": borrowed,
        "books_by_genre": dict(genres),
        "most_prolific_author": most_prolific
    }