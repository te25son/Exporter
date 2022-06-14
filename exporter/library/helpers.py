from flask import request, session, redirect, url_for, current_app
from functools import wraps
from typing import Callable, Any
from .context import AuthContext, MainContext


def auth_action(func: Callable[..., Any]):
    """
    Decorator to be used with auth views. Generates
    a Context based on the incoming function's name, so
    dynamically creates the path to the views template.
    """

    @wraps(func)
    def wrapper():
        return func(AuthContext(request=request, template_name=func.__name__))

    return wrapper


def main_action(func: Callable[..., Any]):
    """
    Decorator to be used with main views. Generates
    a Context based on the incoming function's name, so
    dynamically creates the path to the views template.
    """

    @wraps(func)
    def wrapper():
        return func(MainContext(request=request, template_name=func.__name__))

    return wrapper


def no_direct_url_access(func: Callable[..., Any]):
    """
    Decorate that prevents direct access of a view/endpoint.

    Overriden when TESTING is configured to on.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.referrer or current_app.config["TESTING"]:
            return func(*args, **kwargs)
        return redirect(url_for("main.home"))

    return wrapper


def login_required(func: Callable[..., Any]):
    """
    Decorator that requires a user to be logged in.
    Non logged in users are redirected to the login page.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            return func(*args, **kwargs)
        return redirect(url_for("auth.login"))

    return wrapper


def logged_in_redirect(func: Callable[..., Any]):
    """
    Decorator that redirects a user to the home page
    if the user is already logged in.
    Used on the login and signup views since it does
    not make sense for a logged in user to access
    these views if they're already logged in.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            return redirect(url_for("main.home"))
        return func(*args, **kwargs)

    return wrapper
