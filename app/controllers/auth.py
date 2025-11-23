from bottle import LocalRequest, LocalResponse
from dotenv import load_dotenv
from .db.AuthController import AuthController, IAcessToken, IRefreshToken
from cryptography.fernet import Fernet
import os
import json
from datetime import datetime


load_dotenv()
cipher = Fernet(os.getenv('SECRET_KEY'))


class Auth:
    @staticmethod
    def get_token_pair(request: LocalRequest) -> tuple[IAcessToken | None, IRefreshToken | None]:

        encrypted_refresh_token = request.get_cookie("refresh-token")
        encrypted_access_token = request.get_cookie("access-token")

        irefresh_token = Auth.decrypt_token(encrypted_refresh_token)
        iaccess_token = Auth.decrypt_token(encrypted_access_token)

        refresh_token = None if irefresh_token == None else IRefreshToken(
            irefresh_token["token_id"], irefresh_token["user_id"], irefresh_token["family"], irefresh_token["expiry_date_iso"])

        access_token = None if iaccess_token == None else IAcessToken(
            iaccess_token["user_id"], iaccess_token["role"], iaccess_token["expiry_date_iso"])

        return access_token, refresh_token

    @staticmethod
    def encrypt_token(object: dict) -> str:

        json_str = json.dumps(object)
        json_bytes = json_str.encode()

        encrypted_token_bytes = cipher.encrypt(json_bytes)
        encrypted_token = encrypted_token_bytes.decode()

        return encrypted_token

    @staticmethod
    def decrypt_token(encrypted_token: str) -> dict:
        if encrypted_token == None:
            return None

        encrypted_token_bytes = encrypted_token.encode()

        decrypted_token_bytes = cipher.decrypt(encrypted_token_bytes)
        decrypted_token = decrypted_token_bytes.decode()

        token_dict = json.loads(decrypted_token)

        return token_dict

    @staticmethod
    def get_userid(request: LocalRequest) -> str | None:
        access_token, _ = Auth.get_token_pair(request)

        return access_token.user_id

    @staticmethod
    def generate_token_pair(user_id, response: LocalResponse, family=None) -> bool:
        refresh_token = AuthController.generate_refresh_token(user_id, family)
        encrypted_refresh_token = Auth.encrypt_token(refresh_token.toDict())

        access_token = AuthController.generate_access_token(user_id)
        encrypted_access_token = Auth.encrypt_token(access_token.toDict())

        access_token_expiry = datetime.fromisoformat(
            access_token.expiry_date_iso)
        refresh_token_expiry = datetime.fromisoformat(
            refresh_token.expiry_date_iso)

        access_token_timedelta = access_token_expiry - datetime.now()
        refresh_token_timedelta = refresh_token_expiry - datetime.now()

        cookie_settings = {
            "httponly": True,
            "secure": True,
            "samesite": "Lax"
        }

        response.set_cookie("access-token", encrypted_access_token,
                            maxage=int(access_token_timedelta.total_seconds()), **cookie_settings)
        response.set_cookie(
            "refresh-token", encrypted_refresh_token, maxage=int(refresh_token_timedelta.total_seconds()), **cookie_settings)

        return True

    @staticmethod
    def verify_authentication(request: LocalRequest, response: LocalResponse) -> bool:

        access_token, refresh_token = Auth.get_token_pair(request)

        if access_token != None and datetime.now() < datetime.fromisoformat(access_token.expiry_date_iso):
            return True

        if refresh_token == None or datetime.now() > datetime.fromisoformat(refresh_token.expiry_date_iso):
            # Refresh token expired, requires relogin
            return False

        # Access token expired, but refresh_token valid, fetch new one
        if AuthController.verify_refresh_token(refresh_token.token_id):
            # Valid refresh token, generate new token pair
            Auth.generate_token_pair(refresh_token.user_id, response)
            return True

        else:
            # Session nuked, requires relogin
            return False

    @staticmethod
    def end_session(request: LocalRequest, response: LocalResponse):
        _, refresh_token = Auth.get_token_pair(request)

        if refresh_token != None:
            AuthController.end_session(refresh_token.family)

        response.set_cookie("access-token", "", maxage=0)
        response.set_cookie("refresh-token", "", maxage=0)
