from sqlalchemy import create_engine
from app.book import Book
from sqlalchemy.orm import sessionmaker

from app.user import User

# Define the SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create tables based on the defined models
Book.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)




# Create a sessionmaker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
