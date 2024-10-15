from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

# SQLAlchemy Book model
class Book(Base):
    __tablename__ = 'books_book'
    id = Column(Integer, primary_key=True, index=True)
    download_count = Column(Integer)
    gutenberg_id = Column(Integer)
    media_type = Column(String)
    title = Column(String)

class BookAuthorAssociation(Base):
    __tablename__ = 'books_book_authors'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    author_id = Column(Integer, ForeignKey('books_author.id'))

class Author(Base):
    __tablename__ = 'books_author'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)

    # Relationship to book-author association
    books = relationship('BookAuthorAssociation', backref='author')

class BookLanguagesAssociation(Base):
    __tablename__ = 'books_book_languages'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    language_id = Column(Integer, ForeignKey('books_language.id'))

class Language(Base):
    __tablename__ = 'books_language'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    # Relationship to book-author association
    books = relationship('BookLanguagesAssociation', backref='language')

class BookSubjectsAssociation(Base):
    __tablename__ = 'books_book_subjects'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    subject_id = Column(Integer, ForeignKey('books_subject.id'))

class Subject(Base):
    __tablename__ = 'books_subject'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Relationship to book-author association
    books = relationship('BookSubjectsAssociation', backref='subject')

class BookShelfAssociation(Base):
    __tablename__ = 'books_book_bookshelves'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    bookshelf_id = Column(Integer, ForeignKey('books_bookshelf.id'))

class BookShelf(Base):
    __tablename__ = 'books_bookshelf'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Relationship to book-author association
    books = relationship('BookShelfAssociation', backref='bookshelf')

class BookFormat(Base):
    __tablename__ = 'books_format'

    id = Column(Integer, primary_key=True, index=True)
    mime_type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    book_id = Column(Integer, index=True)


