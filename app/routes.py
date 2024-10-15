from fastapi import FastAPI
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.schemas import BookResponse
from app.crud import filter_books
from app.config import get_db

# Initialize API router
router = APIRouter()

app = FastAPI(swagger_ui_parameters={"deepLinking": False})

# GET /books endpoint
@router.get("/books", response_model=BookResponse)
def get_books(book_ids: list = Query(None),
              title: str = None, author_name: str = Query(None),language: str = Query(None),
              topic: str = Query(None), mime_type: str =Query(None),
              limit: int = 25, offset: int = 0, db: Session = Depends(get_db)):
    # Validate that limit does not exceed 25
    if limit > 25:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 25")

    # Fetch books with applied filters
    total_books, books = filter_books(db, book_ids=book_ids, title=title, author_name=author_name, language=language, topic=topic, mime_type=mime_type, limit=limit, offset=offset)

    # Format the book objects
    books_list = []
    for book in books:

        books_list.append({
            "id":book.id,
            "title": book.title,
            "download_count":book.download_count,
            "gutenberg_id":book.gutenberg_id,
            "authors":book.authors,
            "language":book.language,
            "subject":book.subject,
            "bookshelf":book.bookshelf,
            "mime_type":book.mime_type
        })

    return {"totalBooks": total_books, "books": books_list}
