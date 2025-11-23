from .database import db
from .models.User import User, RefreshToken
import bcrypt
import datetime
from peewee import DoesNotExist, IntegrityError, ModelSelect


class UserController:

    @db.atomic()
    @staticmethod
    def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
        email = email.lower()
        password_bytes = password.encode('utf-8')
        password_hash_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        password_hash = password_hash_bytes.decode('utf-8')

        try:
            User.create(name=name, email=email, password_hash=password_hash)
        except IntegrityError:
            return (False, "Email already exists")
        except Exception:
            return (False, "Request failed, try again.")

        return (True, "")

    @db.atomic()
    @staticmethod
    def login(email: str, password: str) -> tuple[bool, str | User]:
        """
        Return types
            (True, user_id) on success
            (False, "Error message string") on failure

        """

        try:
            login_user: User = User.get(email=email)
        except DoesNotExist:
            return (False, "User not found")

        password_bytes = password.encode("utf-8")
        password_hash_bytes = login_user.password_hash.encode("utf-8")

        if not (bcrypt.checkpw(password_bytes, password_hash_bytes)):
            return (False, "Wrong password")

        return (True, login_user.id)
