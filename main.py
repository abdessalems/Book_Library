# main.py
from sqlite3 import IntegrityError
from typing import List, Optional
from app.database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.book import Book, BookCreate
from app.book_service import BookService
from app.security import Security
from app.user import User
from app.user_service import UserService



""" # from app.database import Base, engine

 Create all tables
Base.metadata.create_all(bind=engine) """


app = FastAPI()

# Define a constant for the error message
BOOK_NOT_FOUND_ERROR = "Book not found"



# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books/", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    """
    Endpoint to get all books.
    """
    return BookService().get_books(db)




@app.post("/books/")
def create_book(title: str, author: str, year: int, photo_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Endpoint to create a new book.
    """
    return BookService().create_book(db, title=title, author=author, year=year, photo_url=photo_url)


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a book by ID.
    """
    book = BookService().get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=BOOK_NOT_FOUND_ERROR)  
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, title: str, author: str, year: int, photo_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Endpoint to update a book.
    """
    updated_book = BookService().update_book(db, book_id, title, author, year, photo_url)
    if not updated_book:
        raise HTTPException(status_code=404, detail=BOOK_NOT_FOUND_ERROR)  # Use constant here
    return updated_book





# Modify the POST endpoint to accept request body parameters
@app.post("/books/body")
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new book.
    """
    return BookService().create_book(
        db,
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        photo_url=book_data.photo_url
    )

# Modify the PUT endpoint to accept request body parameters
@app.put("/books/body/{book_id}")
def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to update a book.
    """
    updated_book = BookService().update_book(
        db,
        book_id,
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        photo_url=book_data.photo_url
    )
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book




@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a book.
    """
    if not BookService().delete_book(db, book_id):
        raise HTTPException(status_code=404, detail=BOOK_NOT_FOUND_ERROR)  # Use constant here
    return {"message": "Book deleted successfully"}


# In main.py
@app.post("/signup/")
def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user.
    """
    hashed_password = Security.get_password_hash(password)
    return UserService().create_user(db, username=username, email=email, hashed_password=hashed_password)







@app.post("/login/")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user.
    """
    user = UserService().authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"message": "Login successful", "user_id": user.id}



from app.security import Security

@app.post("/signup/findError")
async def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    try:
        # Hash the password
        hashed_password = Security.get_password_hash(password)
        
        # Create a new user instance with the hashed password
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        
        # Add user to the database session
        db.add(new_user)
        
        # Commit the transaction to persist the user in the database
        db.commit()
        
        # Return the created user
        return new_user
    except IntegrityError as e:
        # Rollback the transaction in case of an error
        db.rollback()
        
        # If the error is due to duplicate username or email, return a 400 response
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        # For other integrity errors, return a 500 response
        raise HTTPException(status_code=500, detail="Failed to create user")
