from .database import db
from .models.User import User, RefreshToken, generate_expiry_date
import datetime
from peewee import DoesNotExist, IntegrityError, ModelSelect
from dataclasses import dataclass, asdict
import uuid


@dataclass
class IRefreshToken:
    token_id: str
    user_id: str
    family: str
    expiry_date_iso: str

    def toDict(self):
        return asdict(self).copy()


@dataclass
class IAcessToken:
    user_id: str
    role: str
    expiry_date_iso: str

    def toDict(self):
        return asdict(self).copy()


class AuthController:

    @db.atomic()
    @staticmethod
    def generate_refresh_token(user_id: str, family=None):
        token_family = uuid.uuid4()

        if family != None:
            token_family = family

        try:
            refresh_token: RefreshToken = RefreshToken.create(
                user=user_id, family=token_family)
        except Exception as e:
            print("Couldn't create token.")
            print(e)

        expiry_date: datetime.datetime = refresh_token.expiry_date
        iso_expiry_date = expiry_date.isoformat()

        irefresh_token = IRefreshToken(refresh_token.id,
                                       str(refresh_token.user.id), str(refresh_token.family), iso_expiry_date)

        return irefresh_token

    @db.atomic()
    @staticmethod
    def generate_access_token(user_id: str):
        try:
            user: User = User.get_by_id(user_id)
        except Exception as e:
            print("Couldn't fetch user.")
            print(e)

        access_token = IAcessToken(
            str(user.id), user.role, generate_expiry_date(15).isoformat())

        return access_token

    @db.atomic()
    @staticmethod
    def verify_refresh_token(token_id: str) -> bool:

        refresh_token: RefreshToken = RefreshToken.get_by_id(token_id)

        if not refresh_token.is_used:
            refresh_token.is_used = True
            refresh_token.save()

            return True

        # Someone tried to reuse a refresh token, nuke session
        user = refresh_token.user
        user_tokens: ModelSelect = user.tokens
        user_tokens.where(RefreshToken.family == refresh_token.family)

        for token in user_tokens:
            token: RefreshToken
            token.delete()

        return False

    @db.atomic()
    @staticmethod
    def end_session(family: str):
        related_tokens: ModelSelect = RefreshToken.select().where(
            RefreshToken.family == family)

        for token in related_tokens:
            token: RefreshToken
            token.delete()
