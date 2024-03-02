# user_service.py

from sqlalchemy.orm import Session
from app.user import User
from passlib.context import CryptContext

class UserService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, db: Session, username: str, email: str, hashed_password: str) -> User:
        """
        Create a new user and return the created user object.
        """
        user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> User:
        """
        Authenticate a user and return the user object if authenticated, else return None.
        """
        user = db.query(User).filter(User.email == email).first()
        if user and self.verify_password(password, user.hashed_password):
            return user
        return None

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify the plain password against the hashed password.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
