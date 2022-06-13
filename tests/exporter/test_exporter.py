import pytest

from typing import List
from random import randint
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from exporter import settings


class TestExporter:
    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, client: FlaskClient, templates_rendered: List):
        self.client = client
        self.templates_rendered = templates_rendered

    @pytest.fixture()
    def user_session(self):
        with self.client.session_transaction() as session:
            session["username"] = "Test"

    @pytest.fixture()
    def special_user_session(self):
        with self.client.session_transaction() as session:
            session["username"] = settings.DUMMY_ADMIN_USERNAME

    @pytest.mark.parametrize("valid_ids", [True, False])
    def test_export_with_valid_user(self, special_user_session, valid_ids):
        response = self._export_post_response(valid_ids)

        assert response.status_code == 200
        assert response.json["success"] == valid_ids

    @pytest.mark.parametrize("valid_ids", [True, False])
    def test_export_with_valid_ids_invalid_user(self, user_session, valid_ids):
        response = self._export_post_response(valid_ids)

        assert response.status_code == 200
        assert self.templates_rendered[0].name == "main/invalid.html"

    def _export_post_response(self, valid_ids) -> TestResponse:
        form_data = {
            "annotation_id": str(randint(1, 1000))
            if not valid_ids
            else settings.VALID_ANNOTATION_ID,
            "queue_id": str(randint(1, 1000))
            if not valid_ids
            else settings.VALID_QUEUE_ID,
        }
        return self.client.post(url_for("main.export"), data=form_data)
