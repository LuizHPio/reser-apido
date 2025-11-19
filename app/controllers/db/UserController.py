from .database import db
from .models.User import User, AuthToken
import bcrypt
import datetime
from peewee import DoesNotExist, IntegrityError, ModelSelect


class UserController:
    @db.atomic()
    @staticmethod
    def is_logged_in(session_id, session_token) -> bool:
        current_user = User.get(User.id == session_id)
        tokens_query: ModelSelect = current_user.tokens
        tokens_query = tokens_query.where(AuthToken.token == session_token)
        token_number = tokens_query.count()

        if token_number < 1:
            return False

        for token in tokens_query:
            token: AuthToken
            if token.expirity_date > datetime.datetime.now():
                return True

        return False

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
            (True, AuthToken) on success
            (False, "Error message string") on failure

        """
        email = email

        try:
            print(email)
            login_user: User = User.get(email=email)
        except DoesNotExist:
            return (False, "User not found")

        password_bytes = password.encode("utf-8")
        password_hash_bytes = login_user.password_hash.encode("utf-8")

        if not (bcrypt.checkpw(password_bytes, password_hash_bytes)):
            return (False, "Wrong password")

        user_token = AuthToken.create(user=login_user)
        return (True, user_token)

    @db.atomic()
    @staticmethod
    def logout(session_id, session_token) -> bool:
        try:
            user_instance = User.get_by_id(session_id)
            tokens: ModelSelect = user_instance.tokens
            selected_token: ModelSelect = tokens.where(
                AuthToken.token == session_token)

            for token in selected_token:
                AuthToken.delete_by_id(token.id)

        except Exception as e:
            print("Couldn't delete AuthToken")
            print(e)
            return False

        return True
