# user.py
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    """
    Data model to represent a user in the database.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
