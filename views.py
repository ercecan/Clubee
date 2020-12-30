from flask import Flask, render_template, current_app, abort, redirect, request, url_for, flash, session
from datetime import datetime
from forms import LoginForm, AdminLoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, login_fresh, current_user  #login_fresh returns true if the login is fresh(yeni)
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher


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
        print("as")
        abort(404)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    db = current_app.config["db"]
    clubs = db.get_clubs()
    return render_template("clubs.html", clubs=clubs)


def anns_page():  #announcements page
    db = current_app.config["db"]
    announcements = db.get_announcements
    return render_template("announcements.html", announcements=announcements)


def club_page(club_key):
    db = current_app.config["db"]
    club = db.get_club(club_key)
    if club is None:
        abort(404)
    return render_template("club.html", club=club)


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
