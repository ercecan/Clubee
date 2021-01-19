from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2
from config import Config

connection = dbapi2.connect(Config.db_url)  #sslmode='require' for heroku


class User(UserMixin):
    def __init__(self,
                 password,
                 id=None,
                 nickname=None,
                 student_id=None,
                 email=None,
                 name=None,
                 surname=None,
                 department=None,
                 gender=None):
        self.id = id
        self.email = email
        self.name = name
        self.surname = surname
        self.student_id = student_id
        self.nickname = nickname
        self.department = department
        self.password = password
        self.gender = gender
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.nickname if self.is_admin == True else self.student_id  #if the user is admin, return the username of admin, if not return the student number of the student

    @property
    def is_active(self):
        return self.active

    def adduser(self):
        """
        registers user to the database
        """
        user_data = {
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'student_id': self.student_id,
            'department': self.department,
            'password': self.password,
            'gender': self.gender
        }

        try:
            with connection.cursor() as cursor:
                register_statement = """INSERT INTO users (name, surname, student_id, email, department, password_hash,gender)
                                            VALUES (%(name)s, %(surname)s, %(student_id)s, %(email)s, %(department)s, %(password)s,%(gender)s)
                                        RETURNING id;"""
                cursor.execute(register_statement, user_data)
                connection.commit()
                user_id = cursor.fetchone()[0]
        except (Exception, dbapi2.Error) as error:

            print("Error while connecting to PostgreSQL: {}".format(error))


def get_user_by_id(id=None):
    """
    returns a user by id
    """
    if id:
        with connection.cursor() as cursor:
            q = """ SELECT * FROM users WHERE id = %(id)s """
            cursor.execute(q, {'id': id})
            _user = cursor.fetchone()

            if _user:
                _user = User(id=_user[0],
                             email=_user[1],
                             name=_user[2],
                             surname=_user[3],
                             student_id=_user[4],
                             department=_user[5],
                             password=_user[6],
                             gender=_user[7]) if _user[6] else None
            if _user:
                _user.is_admin = False  #user.student_id in current_app.config["ADMIN_USERS"]
                return _user
            else:
                return None


def get_user(user_id=None, email=None):
    """
    returns a user by student id or email
    """
    try:
        with connection.cursor() as cursor:
            if email:
                q = """select * from users where email = %(email)s"""
                data = {'email': str(email)}
                cursor.execute(q, data)
                user = cursor.fetchone()
                if user:
                    return user
                return None
            _user = []
            print("getuser")
            get_user_statement = """SELECT * FROM users WHERE student_id = %(user_id)s"""
            data = {'user_id': user_id}
            cursor.execute(get_user_statement, data)
            _user = cursor.fetchone()
            if _user:
                user = User(id=_user[0],
                            email=_user[1],
                            name=_user[2],
                            surname=_user[3],
                            student_id=_user[4],
                            department=_user[5],
                            password=_user[6],
                            gender=_user[7]) if _user[6] else None
            if _user:
                user.is_admin = False  #user.student_id in current_app.config["ADMIN_USERS"]
                return user
            get_admin_statement = """SELECT * FROM club_admins WHERE nickname = %(user_id)s"""
            cursor.execute(get_admin_statement, data)
            _admin = cursor.fetchone()
            if _admin:
                admin = User(id=_admin[0],
                             nickname=_admin[1],
                             password=_admin[2])
                if _admin[0] is not None:
                    admin.is_admin = True
                    return admin
            return None
    except (Exception, dbapi2.Error) as error:
        print("Error while getting user: {}".format(error))


def is_member(user_id, club_id):
    """
    checks if a user is a member of the given club
    """
    try:
        with connection.cursor() as cursor:
            check_statement = """SELECT * FROM members WHERE user_id = %(user_id)s AND club_id = %(club_id)s;"""
            data = {'user_id': user_id, 'club_id': club_id}
            cursor.execute(check_statement, data)
            ##connection.commit() bu lazım mı ?
            user_id = cursor.fetchone()
            if user_id:  ##Null değilse yani membersa
                return True
            return False
    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error))


def delete_user(user_id):
    """
    deletes user from the database
    """
    try:
        with connection.cursor() as cursor:
            del_user = """DELETE FROM users WHERE id = {}""".format(
                str(user_id))
            cursor.execute(del_user)
            connection.commit()
    except Exception as e:
        print("Error while deleting user", e)


def update_user(id_, name, surname, student_id, email, gender):
    """
    updates user info
    """
    try:
        with connection.cursor() as cursor:
            update_user_statement = """UPDATE users SET name = %(name)s,surname = %(surname)s, 
            student_id = %(student_id)s, email = %(email)s, gender = %(gender)s WHERE id  = %(id_)s; """
            data = {
                'name': name,
                'surname': surname,
                'student_id': student_id,
                'email': email,
                'gender': gender,
                'id_': str(id_)
            }
            cursor.execute(update_user_statement, data)
            connection.commit()
    except Exception as e:
        print("Error while updating user: ", e)