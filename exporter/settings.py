import os

from distutils.util import strtobool


SECRET_KEY = os.getenv("SECRET_KEY", None)
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///exporter/default.db")
DEBUG = bool(strtobool(os.getenv("DEBUG", "false")))
PASSWORD_HASH = os.getenv("HASH", "sha256")

DUMMY_ADMIN_USERNAME = os.getenv("DUMMY_ADMIN_USERNAME", None)
DUMMY_ADMIN_PASSWORD = os.getenv("DUMMY_ADMIN_PASSWORD", "NotSoSecret")

API_USERNAME = os.getenv("API_USERNAME", "")
API_PASSWORD = os.getenv("API_PASSWORD", "")
VALID_ANNOTATION_ID = os.getenv("VALID_ANNOTATION_ID", None)
VALID_QUEUE_ID = os.getenv("VALID_QUEUE_ID", None)
EXPORT_GET_ENDPOINT_BASE = os.getenv("EXPORT_GET_ENDPOINT_BASE", "")
EXPORT_GET_ENDPOINT_END = os.getenv("EXPORT_GET_ENDPOINT_END", "")
EXPORT_POST_ENDPOINT = os.getenv("EXPORT_POST_ENDPOINT", "")
