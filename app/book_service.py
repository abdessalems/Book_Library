# book_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from .book import Book

class BookService:
    """
    Service class for book-related operations.
    """

    def get_books(self, db: Session) -> List[Book]:
        """
        Get all books from the database.
        """
        return db.query(Book).all()

    def create_book(self, db: Session, title: str, author: str, year: int, photo_url: Optional[str] = None) -> Book:
        """
        Create a new book in the database.
        """
        book = Book(title=title, author=author, year=year, photo_url=photo_url)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def get_book_by_id(self, db: Session, book_id: int) -> Optional[Book]:
        """
        Get a book by its ID from the database.
        """
        return db.query(Book).filter(Book.id == book_id).first()

    def update_book(self, db: Session, book_id: int, title: str, author: str, year: int, photo_url: Optional[str] = None) -> Optional[Book]:
        """
        Update a book in the database.
        """
        book = self.get_book_by_id(db, book_id)
        if book:
            book.title = title
            book.author = author
            book.year = year
            book.photo_url = photo_url
            db.commit()
            db.refresh(book)
        return book

    def delete_book(self, db: Session, book_id: int) -> bool:
        """
        Delete a book from the database.
        """
        book = self.get_book_by_id(db, book_id)
        if book:
            db.delete(book)
            db.commit()
            return True
        return False
