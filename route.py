from app.controllers.application import Application
from app.controllers.registration import Registration
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


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
@app.route('/home')
def helper(info=None):
    status = Registration.is_logged_in(request)
    if not status:
        return redirect("/")

    return ctl.render('home')


@app.route('/register', method=['GET', 'POST'])
def helper(info=None):
    status = Registration.is_logged_in(request)
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
    status = Registration.is_logged_in(request)
    if status:
        return redirect("/home")

    if request.method == "POST":
        email = request.forms.get("email")
        password = request.forms.get("senha")
        return Registration.login_user(response, email, password)

    return ctl.render('login')


@app.route('/logout')
def helper(info=None):
    return Registration.logout_user(request, response)


@app.route('/')
def helper(info=None):
    status = Registration.is_logged_in(request)
    if status:
        return redirect("/home")

    return ctl.render('landing')


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=3000, debug=True)
