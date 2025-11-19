from .db.UserController import UserController, AuthToken, User
from bottle import LocalResponse, LocalRequest, redirect


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
            message: AuthToken
            token_str = message.token
            user: User = message.user
            response.set_cookie("session-token", token_str,
                                expires=message.expirity_date)
            response.set_cookie("session-id", str(user.id),
                                expires=message.expirity_date)
            return redirect("/home")

        return message

    def logout_user(request: LocalRequest, response: LocalResponse):
        session_id = request.get_cookie("session-id")
        session_token = request.get_cookie("session-token")

        status = UserController.logout(session_id, session_token)
        if status:
            response.set_cookie("session-token", "", maxage=0)
            response.set_cookie("session-id", "", maxage=0)
            return redirect("/")

        return

    def is_logged_in(request: LocalRequest):
        session_id = request.get_cookie("session-id")
        session_token = request.get_cookie("session-token")

        if session_token == None or session_id == None:
            return False

        return UserController.is_logged_in(session_id, session_token)
