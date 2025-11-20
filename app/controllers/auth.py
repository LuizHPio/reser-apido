from bottle import LocalRequest, LocalResponse


class Auth:
    @staticmethod
    def get_userid(request: LocalRequest) -> str:
        return request.get_cookie("session-id")
