from app.controllers.application import Application
from app.controllers.managment import Managment
from app.controllers.registration import Registration
from app.controllers.auth import Auth
from bottle import Bottle, route, run, request, static_file, TEMPLATE_PATH
from bottle import redirect, template, response


app = Bottle()
ctl = Application()

TEMPLATE_PATH.append("./app/views/html")

# -----------------------------------------------------------------------------
# Rotas:


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')


# -----------------------------------------------------------------------------
# Suas rotas aqui:
@app.route('/home', name="home")
def helper(info=None):
    status = Auth.verify_authentication(request, response)
    if not status:
        return redirect("/")

    return Application.show_home(request)


@app.route('/my-reserves')
def helper(info=None):
    status = Auth.verify_authentication(request, response)
    if not status:
        return redirect("/")
    return Application.show_reserves(request)


@app.route("/admin/delete/room/<id>", method=["POST"])
def helper(id, info=None):
    return Managment.delete_room(id)


@app.route("/admin/create/room", method=["POST"])
def helper(info=None):
    return Managment.create_room(request)


@app.route("/admin/delete/equipment/<id>", method=["POST"])
def helper(id, info=None):
    return Managment.delete_equipment(id)


@app.route("/admin/create/equipment", method=["POST"])
def helper(info=None):
    return Managment.create_equipment(request)


@app.route("/reservar/sala/<id>")
def helper(id, info=None):
    access_token, _ = Auth.get_token_pair(request)

    return Managment.reserve_room(id, access_token.user_id)


@app.route("/reservar/equipamento/<id>")
def helper(id, info=None):
    return Managment.reserve_equipment(id, request)


@app.route("/liberar/sala/<id>")
def helper(id, info=None):
    return Managment.unreserve_room(id, request)


@app.route("/liberar/equipamento/<id>")
def helper(id, info=None):
    return Managment.unreserve_equipment(id, request)


@app.route('/register', method=['GET', 'POST'])
def helper(info=None):
    status = Auth.verify_authentication(request, response)
    if status:
        return redirect("/home")

    if request.method == "POST":
        email = request.forms.get("email")
        password = request.forms.get("senha")
        name = request.forms.get("nome")
        return Registration.register_user(response, name, email, password)

    return ctl.render('register')


@app.route('/login', method=['GET', 'POST'])
def helper(info=None):
    status = Auth.verify_authentication(request, response)
    if status:
        return redirect("/home")

    if request.method == "POST":
        email = request.forms.get("email")
        password = request.forms.get("senha")
        return Registration.login_user(request, response, email, password)

    return ctl.render('login')


@app.route('/logout')
def helper(info=None):
    return Registration.logout_user(request, response)


@app.route("/admin")
def helper(indo=None):
    status = Auth.verify_authentication(request, response)
    if not status:
        return redirect("/")

    return Application.show_admin(request)


@app.route('/')
def helper(info=None):
    status = Auth.verify_authentication(request, response)
    if status:
        return redirect("/home")

    return ctl.render('landing')


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=3000, debug=True, reloader=True)
