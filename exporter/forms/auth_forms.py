from wtforms import Form, PasswordField, StringField, validators  # type: ignore
from werkzeug.security import check_password_hash
from exporter.components.user_component import UserComponent


Users = UserComponent()


class LoginForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.existing_user = Users.get_by_username(self.username.data)

    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])

    def validate_username(self, field: StringField) -> None:
        if not self.existing_user:
            raise validators.ValidationError("Invalid username.")

    def validate_password(self, field: PasswordField) -> None:
        if not self.existing_user or not check_password_hash(
            self.existing_user.password, field.data
        ):
            raise validators.ValidationError("Invalid password.")


class SignupForm(Form):
    username = StringField(
        "Username", [validators.DataRequired(), validators.Length(min=4, max=20)]
    )
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.Length(min=8),
            validators.equal_to("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Confirm password")

    def validate_username(self, field: StringField) -> None:
        existing_user = Users.get_by_username(field.data)
        if existing_user:
            raise validators.ValidationError("User with that username already exists.")
