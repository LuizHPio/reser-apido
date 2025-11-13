from .db.UserController import UserController
from bottle import LocalResponse


class Registration():
    def register_user(response: LocalResponse, name, email, password):
        status, message = UserController.register_user(name, email, password)

        response.content_type = "application/json"

        if status:
            return {"success": status, "message": "Successfully registered, now login."}

        return {"success": status, "message": message}

    def login_user(response: LocalResponse, email, password):
        status, message = UserController.login(email, password)

        if status:
            response.set_cookie("session-token", message)
