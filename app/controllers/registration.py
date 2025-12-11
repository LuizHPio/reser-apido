from .db.UserController import UserController, RefreshToken, User
from bottle import LocalResponse, LocalRequest, redirect
from .auth import Auth


class Registration():

    @staticmethod
    def register_user(response: LocalResponse, name, email, password):
        status, message = UserController.register_user(name, email, password)

        response.content_type = "application/json"

        if status:
            return {"success": status, "message": "Successfully registered, now login."}

        return {"success": status, "message": message}

    @staticmethod
    def login_user(request: LocalRequest, response: LocalResponse, email, password):
        status, message = UserController.login(email, password)

        if status:
            Auth.generate_token_pair(message, request, response)
            return redirect("/home")

        return message

    @staticmethod
    def logout_user(request: LocalRequest, response: LocalResponse):

        Auth.end_session(request, response)

        return redirect("/")
