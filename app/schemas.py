from pydantic import BaseModel
from typing import List, Optional


class AuthorResponse(BaseModel):
    id: Optional[int]
    name: Optional[str]
    birth_year: Optional[int]
    death_year: Optional[int]

    class Config:
        orm_mode = True

class LanguageResponse(BaseModel):
    id: Optional[int]
    code: Optional[str]

    class Config:
        orm_mode = True

class SubjectResponse(BaseModel):
    id: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True

class BookShelfResponse(BaseModel):
    id: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True

class BookFormatResponse(BaseModel):
    id: Optional[int]
    mime_type: Optional[str]
    url: Optional[str]

    class Config:
        orm_mode = True



# BookSchema with authors defaulting to an empty list if not present
class BookSchema(BaseModel):
    id: int
    title: Optional[str]
    download_count: Optional[int] = None
    gutenberg_id: Optional[int] = None
    authors: Optional[List[AuthorResponse]] = []  # Defaulting to an empty list if no authors
    language: Optional[list[LanguageResponse]] =[]  # Defaulting to an empty list if no language
    subject: Optional[list[SubjectResponse]] =[]
    bookshelf:Optional[list[BookShelfResponse]] = []
    mime_type:Optional[list[BookFormatResponse]] =[]

    class Config:
        orm_mode = True


class BookResponse(BaseModel):
    totalBooks: int
    books: List[BookSchema]

    class Config:
        orm_mode = True
