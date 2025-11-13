from .database import db
from .models.User import User, AuthToken
import bcrypt
from peewee import DoesNotExist, IntegrityError


class UserController:
    @db.atomic()
    @staticmethod
    def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
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
    def login(email: str, password: str) -> tuple[bool, str | AuthToken]:
        """
        Return types
            (True, AuthToken) on success
            (False, "Error message string") on failure

        """
        try:
            login_user: User = User.get(User.email == email)
        except DoesNotExist:
            return (False, "User not found")

        password_bytes = password.encode("utf-8")
        password_hash_bytes = login_user.password_hash.encode("utf-8")

        if not (bcrypt.checkpw(password_bytes, password_hash_bytes)):
            return (False, "Wrong password")

        user_token = AuthToken.create(user=login_user)
        return (True, user_token)
