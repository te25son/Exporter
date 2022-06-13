from flask import Blueprint, redirect, render_template, request, url_for, session
from .library.helpers import auth_action, login_required, logged_in_redirect
from .library.context import Context
from .forms.auth_forms import LoginForm, SignupForm
from .models import UserCreate
from .components.user_component import UserComponent


Users = UserComponent()
auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login", methods=["GET", "POST"])
@logged_in_redirect
@auth_action
def login(context: Context):
    """
    View for logging in a user.

    Users who attempt to access this page while logged
    in are redirected back to the home back.

    Once logged in, a session containing the users
    username is created.
    """
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        session["username"] = form.username.data
        response = redirect(url_for("main.home"))
        response.headers["HX-Request"] = True

        return response
    return render_template(context.template, form=form, is_user=False)


@auth.route("/signup", methods=["GET", "POST"])
@logged_in_redirect
@auth_action
def signup(context: Context):
    """
    View for signing up a user.

    Similar to the login method, a user that attempts to
    access this page while already logged in is redirected
    back to the home page.

    To avoid redirecting a user back to the login page after
    signing up, the method also creates a sesssion with the new
    user's username.
    """
    form = SignupForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        Users.create(UserCreate(username, password))

        session["username"] = username
        response = redirect(url_for("main.home"))
        response.headers["HX-Request"] = True

        return response
    return render_template(context.template, form=form, is_user=False)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
@auth_action
def logout(context: Context):
    """
    View for logging out a user.

    Cannot be accessed unless the user is already logged in.
    """
    if request.method == "POST":
        session.pop("username", None)
        return redirect(url_for("auth.login"))
    return render_template(context.template, is_user=True)
