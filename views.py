from flask import Flask, render_template, current_app, abort, redirect, request, url_for, flash, session
from datetime import datetime
from forms import LoginForm, AdminLoginForm, RegistrationForm, CommentForm, AnnouncementForm, EventForm
from flask_login import LoginManager, login_user, logout_user, login_required, login_fresh, current_user  #login_fresh returns true if the login is fresh(yeni)
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher
import psycopg2 as dbapi2
from user import User
from config import Config
from database import Database
from user import is_member
from datetime import datetime
from models import Announcement, Event
from flask import Response
connection = dbapi2.connect(Config.db_url)  #sslmode='require' for heroku


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


def announcements_page():  #announcements page
    db = current_app.config["db"]
    announcements = db.get_announcements()
    return render_template("announcements.html", announcements=announcements)


def club_page(club_id):
    db = current_app.config["db"]
    club = db.get_club(club_id)
    annonucements = db.get_announcements(club_id)
    events = db.get_events(club_id)
    member = []
    if club is None:
        abort(404)
    if current_user.is_authenticated:
        user_id = current_user.id
        if is_member(club_id=club_id, user_id=user_id):
            member.append(user_id)
            print(member)
    return render_template("club.html",
                           club=club,
                           member=member,
                           announcements=annonucements,
                           events=events)


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
def admin_page():  #announcement ve event sayısını bastır
    if not current_user.is_authenticated:
        abort(401)
        return current_app.login_manager.unauthorized()
    if not current_user.is_admin:
        abort(401)
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                get_admin_announcements_statement = """SELECT * FROM announcements WHERE announcements.club_id = 
                (SELECT club_id FROM club_managers WHERE admin_id = {})""".format(
                    current_user.id)
                cursor.execute(get_admin_announcements_statement)
                announcements = cursor.fetchall()
                get_admin_events_statement = """SELECT * FROM events WHERE events.club_id = 
                (SELECT club_id FROM club_managers WHERE admin_id = {})""".format(
                    current_user.id)
                cursor.execute(get_admin_events_statement)
                events = cursor.fetchall()
                get_club_info_statement = """SELECT name FROM clubs WHERE id = 
                (SELECT club_id FROM club_managers WHERE admin_id = {}) """.format(
                    current_user.id)
                cursor.execute(get_club_info_statement)
                club_name = cursor.fetchone()
                return render_template('admin_page.html',
                                       announcements=announcements,
                                       events=events,
                                       club_name=club_name)
        except (Exception, dbapi2.Error) as error:
            print("Error while getting admin page: {}".format(error))
        return render_template('index.html')
    elif request.method == "POST":
        if 'delete_ann' in request.form:  ##delete announcement button
            form_announcements = request.form.getlist("announcement_sel")
            if not len(form_announcements):  ##if no announcements is selected
                flash('You have not selected any announcements')
                return redirect(url_for('admin_page'))
            try:
                with connection.cursor() as cursor:
                    for ann_id in form_announcements:
                        del_announcements_statement = """DELETE FROM announcements WHERE id = {} """.format(
                            ann_id)
                        cursor.execute(del_announcements_statement)
                    connection.commit()
                    flash('Your selected announcement(s) have been deleted')
                    return redirect(url_for('admin_page'))
            except Exception as e:
                print("Error while deleting announcements: ", e)
        elif 'delete_event' in request.form:  ##delete events button
            form_events = request.form.getlist("event_sel")
            if not len(form_events):  ##if no events is selected
                flash('You have not selected any events')
                return redirect(url_for('admin_page'))
            try:
                with connection.cursor() as cursor:
                    for event_id in form_events:
                        del_events_statement = """DELETE FROM events WHERE id = {} """.format(
                            event_id)
                        cursor.execute(del_events_statement)
                    connection.commit()
                    flash('Your selected event(s) have been deleted')
                    return redirect(url_for('admin_page'))
            except Exception as e:
                print("Error while deleting events: ", e)
        else:
            abort(405)
    """
    db = current_app.config["db"]
    clubs = db.get_clubs()
    return render_template("admin_page.html",
                           events=events,
                           announcements=announcements)
    """


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


def announcement_page(club_id, ann_id):
    db = current_app.config["db"]
    club = db.get_club(club_id)
    if club is None:
        abort(404)
    _announcement = db.get_announcement(ann_id=ann_id)
    if _announcement is None:
        abort(404)
    return render_template("announcement.html", announcement=_announcement)


###burda task="" versen
#sonra if task == ""
#geteventpage
#      if task == "comment"
#url_for(event_page,task="comment")


@login_required
def event_page(club_id, event_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_page'))
    if not is_member(club_id=club_id, user_id=current_user.id):
        return redirect(url_for('clubs_page'))
    if request.method == "GET":
        if True:  #task == "get"
            db = current_app.config["db"]
            club = db.get_club(club_id)
            _event = []
            if club is None:
                abort(404)
            if _event is None:
                abort(404)
            _event, _comment = db.get_event(event_id=event_id)
            form = CommentForm()
            return render_template("event.html",
                                   form=form,
                                   event=_event,
                                   comments=_comment)
    elif request.method == "POST":
        if 'delete' in request.form:  #task=="delete"
            print("a")
            form_comments = request.form.getlist("comment_name")
            if not len(form_comments):
                flash('You have not selected any comments')
                return redirect(
                    url_for('event_page', club_id=club_id, event_id=event_id))
            try:
                with connection.cursor() as cursor:
                    del_comment_statement = """DELETE FROM comments WHERE id IN ("""
                    query = ""
                    for comment_id in form_comments:
                        query += str(comment_id) + ","
                    query = query[0:len(query) - 1]
                    query += ")"
                    del_comment_statement += query
                    cursor.execute(del_comment_statement)
                    connection.commit()
                    flash('Your selected comment(s) have been deleted')
                    return redirect(
                        url_for('event_page',
                                club_id=club_id,
                                event_id=event_id))
            except (Exception, dbapi2.Error) as error:
                print("Error while connecting to PostgreSQL: {}".format(error))
        form = CommentForm()
        if form.validate_on_submit():
            content = form.data["content"]
            comment_data = {
                'event_id': event_id,
                'user_id': current_user.id,
                'content': content,
                'created_at': datetime.now()
            }
            try:
                with connection.cursor() as cursor:
                    add_comment_statement = """INSERT INTO comments (event_id, user_id, content, created_at) 
                                                VALUES (%(event_id)s,%(user_id)s,%(content)s,%(created_at)s)"""
                    cursor.execute(add_comment_statement, comment_data)
                    # get_event_statement = """SELECT * FROM events where event_id = %(event_id)i"""
                    # data = {'event_id': event_id}
                    # cursor.execute(get_event_statement, data)
                    # _event = cursor.fetchone()
                    connection.commit()
                    flash('Your comment has been posted')
                    #comment_id = cursor.fetchone()[0]
                    return redirect(
                        url_for('event_page',
                                club_id=club_id,
                                event_id=event_id))
            except (Exception, dbapi2.Error) as error:
                print("Error while connecting to PostgreSQL: {}".format(error))
        else:
            return redirect(
                url_for('event_page', club_id=club_id, event_id=event_id))
    else:
        abort(405)  #Method not allowed


# def comment(user_id, event_id):
#     if not current_user.is_authenticated:
#         return redirect(url_for('login_page'))
#     form = CommentForm()
#     if form.validate_on_submit():
#         content = form.data["content"]
#         comment_data = {
#             'event_id': event_id,
#             'user_id': user_id,
#             'content': content,
#             'created_at': datetime.now()
#         }
#         try:
#             with dbapi2.connect(Config.db_url) as connection:
#                 with connection.cursor() as cursor:
#                     add_comment_statement = """INSERT INTO comments (event_id, user_id, content, created_at)
#                                                 VALUES (%(event_id)s,%(user_id)s,%(content)s,%(created_at)s)"""
#                     cursor.execute(add_comment_statement, comment_data)
#                     get_event_statement = """SELECT * FROM events where event_id = %(event_id)s"""
#                     _event = cursor.fetchone()
#                     connection.commit()
#                     #comment_id = cursor.fetchone()[0]
#                     return render_template('event.html', event=_event)
#         except (Exception, dbapi2.Error) as error:
#             print("Error while connecting to PostgreSQL: {}".format(error))
#         flash('Your comment has been posted')
#         return redirect(url_for('login'))
#     else:
#         return redirect(url_for('clubs_page'))


@login_required
def add_announcement_page():
    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    form = AnnouncementForm()
    if form.validate_on_submit():
        header = form.data["header"]
        content = form.data["content"]
        image = form.data["image"]
        ann = Announcement(header, content, image)
        db = current_app.config["db"]
        db.add_announcement(ann, current_user.id)
        flash('announcement added to the database')
        return redirect(url_for("admin_page"))
    return render_template("ann_add.html", form=form)


@login_required
def edit_announcement_page(ann_id):

    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    form = AnnouncementForm()
    db = current_app.config["db"]
    announcement = db.get_announcement(ann_id)
    if form.validate_on_submit():
        header = form.data["header"]
        content = form.data["content"]
        image = form.data["image"]
        _announcement = Announcement(header=header,
                                     content=content,
                                     image=image)
        db.update_announcement(ann_id=ann_id, announcement=_announcement)
        return redirect(url_for("admin_page"))
    form.header.data = announcement[2]
    form.content.data = announcement[3]
    form.image.data = announcement[4]
    return render_template("ann_edit.html", form=form)


@login_required
def add_event_page():
    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    form = EventForm()
    if form.validate_on_submit():
        header = form.data["header"]
        content = form.data["content"]
        image = form.data["image"]
        date = form.data["date"]
        event = Event(header=header, content=content, date=date, image=image)
        db = current_app.config["db"]
        db.add_event(event, current_user.id)
        flash('event added to the database')
        return redirect(url_for("admin_page"))
    return render_template("event_add.html", form=form)


@login_required
def edit_event_page(event_id):
    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    try:
        form = EventForm()
        db = current_app.config["db"]
        event = db.get_event_info(event_id)
        if form.validate_on_submit():
            header = form.data["header"]
            content = form.data["content"]
            image = form.data["image"]
            date = form.data["date"]
            _event = Event(header=header,
                           content=content,
                           date=date,
                           image=image)
            db.update_event(event_id=event_id, event=_event)
            return redirect(url_for("admin_page"))
        form.header.data = event[2]
        form.content.data = event[3]
        form.image.data = event[4]
        return render_template("event_edit.html", form=form)
    except Exception as e:
        print(e)


"""
@login_required
def edit_announcement():
"""
"""
@login_required
def delete_announcement():
"""
"""
@login_required
def add_event():
"""
"""
@login_required
def edit_event():
"""
"""
@login_required
def delete_event():
"""