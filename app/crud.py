from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, and_
from app.models import Book, Author, BookAuthorAssociation, Language, BookLanguagesAssociation, Subject \
                     , BookSubjectsAssociation, BookShelf, BookShelfAssociation, BookFormat
# Helper function to filter books
def filter_books(db: Session, book_ids: list = None,
                 title: str = None, author_name:str =None, language:str =None, topic:str = None, mime_type:str = None, limit: int = 25, offset: int = 0):
    query = db.query(Book)

    if book_ids:
        query = query.filter(Book.gutenberg_id.in_(book_ids))

    if title:
         query = query.filter(Book.title.ilike(f"%{title}%"))

    if author_name:
        query = (
            query
            .join(BookAuthorAssociation, Book.id == BookAuthorAssociation.book_id)
            .join(Author, Author.id == BookAuthorAssociation.author_id)
            .filter(Author.name.ilike(f"%{author_name}%"))
        )

    if language:
        languages = [t.strip() for t in language.split(",")]
        language_filters = or_(
            *[Language.code.ilike(f"%{t}%") for t in languages],  # Match each language in language
        )
        query = (
            query
            .join(BookLanguagesAssociation, Book.id == BookLanguagesAssociation.book_id)
            .join(Language, Language.id == BookLanguagesAssociation.language_id)
            .filter(language_filters)
        )

    if topic:
        topics = [t.strip() for t in topic.split(",")]

        # Construct the filter using `or_` for subjects and bookshelves
        topic_filters = or_(
            *[Subject.name.ilike(f"%{t}%") for t in topics],  # Match each topic in subject
            *[BookShelf.name.ilike(f"%{t}%") for t in topics]  # Match each topic in bookshelf
        )

        query = (
            query
            .outerjoin(BookSubjectsAssociation, Book.id == BookSubjectsAssociation.book_id)
            .outerjoin(Subject, Subject.id == BookSubjectsAssociation.subject_id)
            .outerjoin(BookShelfAssociation, Book.id == BookShelfAssociation.book_id)
            .outerjoin(BookShelf, BookShelf.id == BookShelfAssociation.bookshelf_id)
            .filter(topic_filters)
        )

    if mime_type:
        query = (
            query
            .join(BookFormat, Book.id == BookFormat.book_id)
            .filter(BookFormat.mime_type.ilike(f"%{mime_type}%"))
        )

    # Sort by downloads (popularity) in descending order
    query = query.order_by(desc(Book.download_count))

    total_books = query.count()
    books = query.offset(offset).limit(limit).all()
    for book in books:
        book.authors = (
               db.query(Author)
               .join(BookAuthorAssociation, Author.id == BookAuthorAssociation.author_id)
               .filter(BookAuthorAssociation.book_id == book.id).all()
        )
        book.language =(
            db.query(Language)
            .join(BookLanguagesAssociation, Language.id == BookLanguagesAssociation.language_id)
            .filter(BookLanguagesAssociation.book_id == book.id).all()
        )
        book.subject = (
            db.query(Subject)
            .join(BookSubjectsAssociation, Subject.id == BookSubjectsAssociation.subject_id)
            .filter(BookSubjectsAssociation.book_id == book.id).all()
        )
        book.bookshelf = (
            db.query(BookShelf)
            .join(BookShelfAssociation, BookShelf.id == BookShelfAssociation.bookshelf_id)
            .filter(BookShelfAssociation.book_id == book.id).all()
        )
        book.mime_type =(
            db.query(BookFormat)
            .filter(BookFormat.book_id == book.id).all()
        )
    return total_books, books