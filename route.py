from app.controllers.application import Application
from app.controllers.managment import Managment
from app.controllers.registration import Registration
from app.controllers.auth import Auth
from app.controllers.managment import Managment
from bottle import Bottle, route, request, static_file, TEMPLATE_PATH, BaseRequest
from bottle import redirect, response
import socketio
import eventlet

bottle_app = Bottle()
ctl = Application()
sio = socketio.Server(async_mode='eventlet')

# Maps user_id to socket id
user_sessions: dict[str, int] = {}

# setup controllers
Managment.configure(sio, user_sessions)

socketio_app = socketio.WSGIApp(sio, bottle_app)

TEMPLATE_PATH.append("./app/views/html")


@sio.event
def connect(sid, environ):
    handshake_request = BaseRequest(environ)
    user_id = Auth.get_userid(handshake_request)

    if user_id == None:
        return

    user_sessions[user_id] = sid
    print(f"Client connected: socket_id: {sid}, user_id: {user_id}")


@sio.event
def disconnect(sid):
    user_id_to_remove = None

    for (user_id, socket_id) in user_sessions.items():
        if socket_id == sid:
            user_id_to_remove = user_id

    if user_id_to_remove:
        user_sessions.pop(user_id_to_remove)

    print(f"Client disconnected: {sid}")

# -----------------------------------------------------------------------------
# Rotas:


@bottle_app.route('/static/<filepath:path>')  # type: ignore
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


@bottle_app.route('/helper')  # type: ignore
def helper(info=None):
    return ctl.render('helper')


# -----------------------------------------------------------------------------
# Suas rotas aqui:

@bottle_app.route('/home', name="home")  # type: ignore
def serve_home(info=None):
    status = Auth.verify_authentication(request, response)
    if not status:
        return redirect("/")

    return Application.show_home(request)


@bottle_app.route('/my-reserves')  # type: ignore
def serve_reserve(info=None):
    status = Auth.verify_authentication(request, response)
    if not status:
        return redirect("/")
    return Application.show_reserves(request)


@bottle_app.route("/admin/delete/room/<id>", method="POST")  # type: ignore
def api_delete_room(id, info=None):
    return Managment.delete_room(id)


@bottle_app.route("/admin/create/room", method="POST")  # type: ignore
def api_create_room(info=None):
    return Managment.create_room(request)


@bottle_app.route("/admin/delete/equipment/<id>", method="POST")  # type: ignore # nopep8
def api_delete_equipment(id, info=None):
    return Managment.delete_equipment(id)


@bottle_app.route("/admin/create/equipment", method="POST")  # type: ignore
def api_create_equipment(info=None):
    return Managment.create_equipment(request)


@bottle_app.route("/reservar/sala/<id>", method="POST")  # type: ignore
def api_reserve_room(id, info=None):
    access_token, _ = Auth.get_token_pair(request)

    if access_token == None:
        return

    return Managment.reserve_room(id, access_token.user_id)


@bottle_app.route("/liberar/sala/<id>", method="POST")  # type: ignore
def api_unreserve_room(id, info=None):
    return Managment.unreserve_room(id, request, sio)


@bottle_app.route("/reservar/equipamento/<id>", method="POST")  # type: ignore
def api_reserve_equipment(id, info=None):
    return Managment.reserve_equipment(id, request)


@bottle_app.route("/liberar/equipamento/<id>", method="POST")  # type: ignore
def api_unreserve_equipment(id, info=None):
    return Managment.unreserve_equipment(id, request)


@bottle_app.route('/register', method=['GET', 'POST'])  # type: ignore
def serve_registration(info=None):
    status = Auth.verify_authentication(request, response)
    if status:
        return redirect("/home")

    if request.method == "POST":
        # Bottle magic
        email = request.forms.get("email")  # type: ignore
        password = request.forms.get("senha")  # type: ignore
        name = request.forms.get("nome")  # type: ignore
        return Registration.register_user(response, name, email, password)

    return ctl.render('register')


@bottle_app.route('/login', method=['GET', 'POST'])  # type: ignore
def serve_login(info=None):
    status = Auth.verify_authentication(request, response)
    if status:
        return redirect("/home")

    if request.method == "POST":
        # Bottle magic
        email = request.forms.get("email")  # type: ignore
        password = request.forms.get("senha")  # type: ignore
        return Registration.login_user(request, response, email, password)

    return ctl.render('login')


@bottle_app.route('/logout')  # type: ignore
def serve_logout(info=None):
    return Registration.logout_user(request, response)


@bottle_app.route("/admin")  # type: ignore
def serve_admin_page(indo=None):
    status = Auth.verify_authentication(request, response)
    if not status:
        return redirect("/")

    return Application.show_admin(request)


@bottle_app.route('/')  # type: ignore
def serve_landing(info=None):
    status = Auth.verify_authentication(request, response)
    if status:
        return redirect("/home")

    return ctl.render('landing')


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    eventlet.wsgi.server(eventlet.listen(('', 3000)),  # type: ignore
                         socketio_app)
