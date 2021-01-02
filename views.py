from flask import Flask, render_template, current_app, abort, redirect, request, url_for, flash, session
from datetime import datetime
from forms import LoginForm, AdminLoginForm, RegistrationForm
from flask_login import LoginManager, login_user, logout_user, login_required, login_fresh, current_user  #login_fresh returns true if the login is fresh(yeni)
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher
import psycopg2 as dbapi2
from user import User
from config import Config
from database import Database
from user import is_member


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("index.html", day=day_name)


def clubs_page():
    db = current_app.config["db"]
    clubs = db.get_clubs()
    return render_template("clubs.html", clubs=clubs)


@login_required
def myclubs_page():
    if current_user.is_admin:
        print("Admins are not allowed")
        abort(404)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    db = current_app.config["db"]
    clubs = db.get_member_clubs(user_id=current_user.id, )
    return render_template("clubs.html", clubs=clubs)


def anns_page():  #announcements page
    db = current_app.config["db"]
    announcements = db.get_announcements
    return render_template("announcements.html", announcements=announcements)


def club_page(club_key):
    db = current_app.config["db"]
    club = db.get_club(club_key)
    member = []
    if club is None:
        abort(404)
    if current_user.is_authenticated:
        user_id = current_user.id
        club_id = club_key
        if is_member(club_id=club_id, user_id=user_id):
            member.append(user_id)
            print(member)
    return render_template("club.html", club=club, member=member)


def login():
    form = LoginForm()
    if form.validate_on_submit():
        student_id = form.data["username"]
        user = get_user(student_id)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)
    """
        """


"""
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            'Login requested for student with student ID: {}, remember_me={}'.
            format(form.username.data, form.remember_me.data))
        return redirect(url_for('home_page'))
    return render_template('login.html', title='Sign In', form=form)
"""


def logout():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))


def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        nickname = form.data["username"]
        user = get_user(nickname)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                i_am_in = login_user(user, force=True, fresh=False)
                if i_am_in:
                    flash("You have logged in.")
                    next_page = request.args.get("next", url_for("admin_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("admin_login.html",
                           title='Sign In as Admin',
                           form=form)


def admin_logout():
    logout_user()
    flash("You as an admin have logged out.")
    return redirect(url_for("home_page"))


@login_required
def admin_page():
    if not current_user.is_admin:
        abort(401)
    if not current_user.is_authenticated:
        abort(401)
        return current_app.login_manager.unauthorized()
    if not current_user.is_admin:
        abort(401)
    db = current_app.config["db"]
    clubs = db.get_clubs()
    return render_template("admin_page.html", clubs=clubs)


def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.data["name"]
        surname = form.data["surname"]
        student_id = form.data["student_id"]
        email = form.data["email"]
        department = form.data["department"]
        password = form.data["password"]
        password_hash = hasher.hash(password)
        user = User(name=name,
                    surname=surname,
                    student_id=student_id,
                    email=email,
                    department=department,
                    password=password_hash)
        user.adduser()
        flash('Congratulations, you are now a registered user!')
        flash(f'Account Created for {student_id}! Now You Can Login.',
              'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@login_required
def join_club(
    club_id
):  ##club ismiyle selectleyip clubid yi gönder ya da clubs db classı oluştur
    if not current_user.is_authenticated or current_user.is_admin:
        abort(401)
    try:
        with dbapi2.connect(Config.db_url) as connection:
            with connection.cursor() as cursor:
                if not is_member(current_user.id, club_id):
                    join_statement = """INSERT INTO members (user_id, club_id) VALUES (%(user_id)s, %(club_id)s);"""
                    data = {'user_id': current_user.id, 'club_id': club_id}

                    cursor.execute(join_statement, data)
                    ##connection.commit()  bu lazım mı ?
                    #user_id = cursor.fetchone()
                    update_statement = """UPDATE clubs  SET student_count = student_count + 1 WHERE id = %(club_id)s;"""
                    cursor.execute(update_statement, {'club_id': str(club_id)})
                    connection.commit()
                    return redirect(url_for('clubs_page'))
                return redirect(url_for('clubs_page'))
    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error))


@login_required
def leave_club(club_id):
    if not current_user.is_authenticated or current_user.is_admin:
        abort(401)
    try:
        with dbapi2.connect(Config.db_url) as connection:
            with connection.cursor() as cursor:
                if is_member(
                        current_user.id, club_id
                ):  ##returns one if the user is actually a member of the club
                    leave_statement = """DELETE FROM members WHERE user_id = %(user_id)s AND club_id = %(club_id)s;"""
                    data = {'user_id': current_user.id, 'club_id': club_id}
                    cursor.execute(leave_statement, data)
                    ##connection.commit() bu lazım mı ?
                    #user_id = cursor.fetchone()[0]
                    update_statement = """UPDATE clubs SET student_count = student_count - 1 WHERE id = %(club_id)s;"""
                    data = {'club_id': club_id}
                    cursor.execute(update_statement, data)
                    connection.commit()
                    return redirect(url_for('clubs_page'))
                return redirect(url_for('clubs_page'))
    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error))