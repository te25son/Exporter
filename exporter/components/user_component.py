from sqlmodel import Session, select
from werkzeug.security import generate_password_hash
from sqlmodel.sql.expression import Select, SelectOfScalar
from exporter.models import User, UserCreate
from exporter.db import DB
from exporter import settings


# Temp workaround discussed here https://github.com/tiangolo/sqlmodel/issues/189
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


class UserComponent:
    """
    Component that acts a separator between the view and the logic.
    Deals specificaly with logic related to users.
    """

    @staticmethod
    def get_by_username(username: str) -> User | None:
        user: User | None
        with Session(DB) as session:
            query = select(User).where(User.username == username)
            user = session.exec(query).first()
        return user

    @staticmethod
    def create(user: UserCreate) -> User:
        new_user = User(
            username=user.username,
            password=generate_password_hash(user.password, settings.PASSWORD_HASH),
        )

        with Session(DB) as session:
            session.add(new_user)
            session.commit()

        return new_user
