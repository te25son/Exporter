import pytest

from flask import Flask, template_rendered
from exporter.app import create_app


@pytest.fixture(scope="session")
def app():
    """
    Setup the test app. This is executed once per session.
    """
    params = {"TESTING": True, "WTF_CSRF_ENABLED": False}
    _app = create_app(override_settings=params)

    with _app.app_context(), _app.test_request_context():
        yield _app


@pytest.fixture(scope="function")
def client(app: Flask):
    """
    Setup the app client. This is executed for every function.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def templates_rendered(app: Flask):
    """
    Fixture for capturing templates rendered during testing.
    This is executed for every function.

    It requires the 'blinker' library to be installed. See
    https://flask.palletsprojects.com/en/2.1.x/signals/
    """
    templates = []

    def record(sender, template, context, **kwargs):
        templates.append(template)

    template_rendered.connect(record, app)
    try:
        yield templates
    finally:
        template_rendered.disconnect(record, app)
