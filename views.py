from flask import Flask, render_template, current_app, abort, redirect, request, url_for, flash
from datetime import datetime
from forms import LoginForm


def home_page():

    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("index.html", day=day_name)


def clubs_page():
    db = current_app.config["db"]
    clubs = db.get_clubs()
    return render_template("clubs.html", clubs=clubs)


def anns_page():  #announcements page

    anns = [{
        'name': 'ITU ACM',
        'header': 'alumnight',
        'description': 'alumnight today',
    }, {
        'name': 'ITU IEEE',
        'header': 'circuit design',
        'description': 'circuit today',
    }]
    return render_template("announcements.html", anns=anns)


def club_page(name):
    db = current_app.config["db"]
    club = db.get_club(name)
    return render_template("club.html", club=club)


def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)