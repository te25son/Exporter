from dataclasses import dataclass
from sqlmodel import VARCHAR, Column, Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(
        index=True, sa_column=Column("username", VARCHAR, unique=True)
    )
    password: str
    can_export: bool | None = Field(default=False)


@dataclass
class UserCreate:
    username: str
    password: str
