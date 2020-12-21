from flask import Flask, render_template, current_app, abort, redirect, request, url_for, flash
from datetime import datetime
from forms import LoginForm, AdminLoginForm


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("index.html", day=day_name)


def clubs_page():
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
        flash(
            'Login requested for student with student ID: {}, remember_me={}'.
            format(form.username.data, form.remember_me.data))
        return redirect(url_for('home_page'))
    return render_template('login.html', title='Sign In', form=form)


def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        flash('Login requested for admin: {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home_page'))
    return render_template('admin_login.html',
                           title='Sign In as Admin',
                           form=form)
