from sqlmodel import SQLModel, create_engine, Session
from werkzeug.security import generate_password_hash
from .models import User
from exporter import settings


DB = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)


def create_db_and_tables() -> None:
    """
    Initializes the database and creates all the tables using SQLModel.
    Does not recreate tables that already exist in the database.
    """
    SQLModel.metadata.create_all(DB)


def create_dummy_admin() -> None:
    """
    Creates a dummy admin user with permission to export. If the user
    already exists, the method with skip so the app can continue.
    """
    try:
        user = User(
            username=settings.DUMMY_ADMIN_USERNAME,
            password=generate_password_hash(
                settings.DUMMY_ADMIN_PASSWORD, settings.PASSWORD_HASH
            ),
            can_export=True,
        )

        with Session(DB) as session:
            session.add(user)
            session.commit()
    except:
        pass
