from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2
from config import Config


class User(UserMixin):
    def __init__(
        self,
        password,
        id=None,
        nickname=None,
        student_id=None,
        email=None,
        name=None,
        surname=None,
        department=None,
    ):
        self.id = id
        self.email = email
        self.name = name
        self.surname = surname
        self.student_id = student_id
        self.nickname = nickname
        self.department = department
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.nickname if self.is_admin == True else self.student_id  #if the user is admin, return the username of admin, if not return the student number of the student

    @property
    def is_active(self):
        return self.active

    def adduser(self):
        user_data = {
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'student_id': self.student_id,
            'department': self.department,
            'password': self.password
        }

        try:
            with dbapi2.connect(Config.db_url) as connection:
                with connection.cursor() as cursor:
                    register_statement = """INSERT INTO users (name, surname, student_id, email, department, password_hash)
                                                VALUES (%(name)s, %(surname)s, %(student_id)s, %(email)s, %(department)s, %(password)s)
                                            RETURNING id;"""
                    cursor.execute(register_statement, user_data)
                    connection.commit()
                    user_id = cursor.fetchone()[0]
        except (Exception, dbapi2.Error) as error:

            print("Error while connecting to PostgreSQL: {}".format(error))


def get_user(user_id):
    print("getuser")
    password = current_app.config["PASSWORDS"].get(user_id)
    user = User(student_id=user_id, password=password) if password else None
    if user is not None:
        user.is_admin = False  #user.student_id in current_app.config["ADMIN_USERS"]
        return user

    password = current_app.config["ADMIN_PASSWORDS"].get(user_id)
    user = User(nickname=user_id, password=password) if password else None
    if user is not None:
        user.is_admin = True  #user.student_id in current_app.config["ADMIN_USERS"]
        return user
    return None


"""
this wont work becuase flask only works with 'get_user' sooooooooooo weird
def get_admin_user(nickname):
    password = current_app.config["ADMIN_PASSWORDS"].get(nickname)
        user = User(nickname=nickname, password=password) if password else None
        if user is not None:
            user.is_admin = True  #user.student_id in current_app.config["ADMIN_USERS"]
        return user
"""