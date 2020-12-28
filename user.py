from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        student_id,
        password,
        email=None,
        name=None,
        surname=None,
        department=None,
    ):
        self.email = email
        self.name = name
        self.surname = surname
        self.student_id = student_id
        self.department = department
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.student_id

    @property
    def is_active(self):
        return self.active


def get_user(user_id):
    password = current_app.config["PASSWORDS"].get(user_id)
    user = User(user_id, password) if password else None
    if user is not None:
        user.is_admin = False  #user.student_id in current_app.config["ADMIN_USERS"]
    return user