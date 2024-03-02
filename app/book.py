# book.py
from typing import Optional
from sqlmodel import Field, SQLModel

class Book(SQLModel, table=True):
    """
    Data model to represent a book in the database.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int
    photo_url: Optional[str] = None  # Field for the URL of the book's photo


from pydantic import BaseModel

# Define a Pydantic model for the request body
class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    photo_url: str =Optional[str]