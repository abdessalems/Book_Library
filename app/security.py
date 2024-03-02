# security.py
from passlib.context import CryptContext

class Security:
    """
    Utility class for security-related operations.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password.
        """
        return Security.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        """
        return Security.pwd_context.verify(plain_password, hashed_password)
