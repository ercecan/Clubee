from flask import Flask, render_template, current_app, abort, redirect, request, url_for, flash, session
from datetime import datetime
from forms import LoginForm, AdminLoginForm, RegistrationForm, CommentForm, AnnouncementForm, EventForm, UserUpdateForm, ClubUpdateForm  #, validate_mail, validate_studentid
from flask_login import LoginManager, login_user, logout_user, login_required, login_fresh, current_user  #login_fresh returns true if the login is fresh(yeni)
from user import get_user, get_user_by_id
from passlib.hash import pbkdf2_sha256 as hasher
import psycopg2 as dbapi2
from user import User, is_member, delete_user, update_user
from config import Config
from database import Database
from models import Announcement, Event
from flask import Response
from upload import allowed_file, ALLOWED_EXTENSIONS  ##necessary functions for uploading
from werkzeug.utils import secure_filename
import os
import base64
from PIL import Image
from io import BytesIO

connection = dbapi2.connect(Config.db_url)  #sslmode='require' for heroku


def home_page():
    """
    the home page ('/') of the application
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    try:
        db = current_app.config["db"]
        announcements = db.get_announcements(all=False)
        with connection.cursor() as cursor:
            # /* alana gore kayıtlı kulup sayısı*/
            st = """select areas.area ,count(clubs.name)from areas left join clubs on clubs.id = areas.club_id group by area"""
            cursor.execute(st)
            club_area_n = cursor.fetchall()
            # /*total kulup sayısı*/
            st = """select count(id) from clubs"""
            cursor.execute(st)
            club_number = cursor.fetchone()
            # /* kuluplere katılan unique ogrenci sayısı */
            st = """select count(distinct user_id) from members"""
            cursor.execute(st)
            unique_member_num = cursor.fetchone()
            # /*toplam kulup katılımı*/
            st = """select sum(student_count) from clubs"""
            cursor.execute(st)
            total_participation = cursor.fetchone()

            # /*tortalama bir kulup katılımı*/
            st = """select avg(student_count) from clubs"""
            cursor.execute(st)
            average_participation = cursor.fetchone()

        return render_template("index.html",
                               announcements=announcements,
                               c_num=club_area_n,
                               c_m=club_number,
                               u_m=unique_member_num,
                               t_p=total_participation,
                               a_p=average_participation)
    except Exception as e:
        print("Error while getting home page: ", e)


def clubs_page():
    """
    in this page all clubs in database are seen
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    try:
        db = current_app.config["db"]
        clubs = db.get_clubs()
        all_areas = []
        cursor = connection.cursor()
        for club in clubs:
            club_id = club[0]
            area_statement = """SELECT area FROM areas WHERE club_id = {}""".format(
                str(club_id))
            cursor.execute(area_statement)
            area = cursor.fetchall()
            areas = []
            for ar in area:
                areas.append(ar[0])
            str1 = " "
            x = str1.join(areas)
            all_areas.append(x)
        # /* alana gore kayıtlı kulup sayısı*/
        st = """select areas.area ,count(clubs.name)from areas left join clubs on clubs.id = areas.club_id group by area"""
        cursor.execute(st)
        club_area_n = cursor.fetchall()
        return render_template("clubs.html",
                               clubs=clubs,
                               areas=all_areas,
                               club_area=club_area_n)
    except Exception as e:
        print("Error while getting clubs page: ", e)


@login_required
def myclubs_page():
    """
    the user will see the joined clubs in this page
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    if current_user.is_admin:
        print("Admins are not allowed")
        abort(404)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    db = current_app.config["db"]
    clubs = db.get_member_clubs(user_id=current_user.id, )
    return render_template("myclubs.html", clubs=clubs)


def announcements_page():  #announcements page
    """
    any user can see the announcements in this page
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    db = current_app.config["db"]
    announcements = db.get_announcements(all=True)
    return render_template("announcements.html", announcements=announcements)


def club_page(club_id):
    """
    a page of a specific club
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
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
    """
    login page and login post function
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    form = LoginForm()
    if form.validate_on_submit():
        student_id = form.data["username"]
        user = get_user(user_id=student_id)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout():
    """
    logs user out of the session
    """
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))


def admin_login():
    """
    logs admins in the session and redirects to their own interface
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    form = AdminLoginForm()
    if form.validate_on_submit():
        nickname = form.data["username"]
        user = get_user(user_id=nickname)
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
    """
    logs admins out of the session
    """
    logout_user()
    flash("You as an admin have logged out.")
    return redirect(url_for("home_page"))


@login_required
def admin_page():  #announcement ve event sayısını bastır
    """
    admins interface where they can add update delete announcements and events
    """
    if not current_user.is_authenticated:
        abort(401)
        return current_app.login_manager.unauthorized()
    if not current_user.is_admin:
        abort(401)
    if request.method == "GET":
        try:
            db = current_app.config["db"]
            anns = db.get_announcements(admin_id=current_user.id)
            evs = db.get_events(admin_id=current_user.id)
            with connection.cursor() as cursor:
                get_club_info_statement = """SELECT name FROM clubs WHERE id =
                (SELECT club_id FROM club_managers WHERE admin_id = {}) """.format(
                    current_user.id)
                cursor.execute(get_club_info_statement)
                club_name = cursor.fetchone()
            return render_template('admin_page.html',
                                   announcements=anns,
                                   events=evs,
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


def register():
    """
    the page where normal users can register and then gain the ability to login
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.data["name"]
        surname = form.data["surname"]
        student_id = form.data["student_id"]
        email = form.data["email"]
        gender = form.data["gender"]
        department = form.data["department"]
        password = form.data["password"]
        password_hash = hasher.hash(password)
        user = User(name=name,
                    surname=surname,
                    student_id=student_id,
                    email=email,
                    department=department,
                    password=password_hash,
                    gender=gender)
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
    """
    a function to make authenticated users be able to join clubs
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    if not current_user.is_authenticated or current_user.is_admin:
        abort(401)
    try:
        with connection.cursor() as cursor:
            if not is_member(current_user.id, club_id):
                join_statement = """INSERT INTO members (user_id, club_id) VALUES (%(user_id)s, %(club_id)s);"""
                data = {'user_id': current_user.id, 'club_id': club_id}
                cursor.execute(join_statement, data)
                #user_id = cursor.fetchone()
                update_statement = """UPDATE clubs  SET student_count = student_count + 1 WHERE id = %(club_id)s;"""
                cursor.execute(update_statement, {'club_id': str(club_id)})
                connection.commit()
                return redirect(url_for('club_page', club_id=club_id))
    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error))


@login_required
def leave_club(club_id):
    """
    a function to make authenticated users be able to leave clubs
    """
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
                update_statement = """UPDATE clubs SET student_count = student_count - 1 WHERE id = %(club_id)s;"""
                data = {'club_id': club_id}
                cursor.execute(update_statement, data)
                connection.commit()
                return redirect(url_for('club_page', club_id=club_id))
            return redirect(url_for('clubs_page'))
    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error))


def announcement_page(club_id, ann_id):
    """
    page of a specific announcement
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
    try:
        db = current_app.config["db"]
        club = db.get_club(club_id)
        if club is None:
            abort(404)
        _announcement = db.get_announcement(ann_id=ann_id)
        if _announcement is None:
            abort(404)
        with connection.cursor() as cursor:
            get_name_statement = "SELECT  clubs.name FROM clubs LEFT JOIN announcements ON clubs.id = announcements.club_id WHERE announcements.club_id = {};".format(
                _announcement[1])
            cursor.execute(get_name_statement)
            club_name = cursor.fetchone()
        return render_template("announcement.html",
                               announcement=_announcement,
                               club_name=club_name[0])
    except Exception as e:
        print("error while getting ann page", e)


@login_required
def event_page(club_id, event_id):
    """
    page of a specific event
    """
    if current_user.is_anonymous:
        pass
    else:
        if current_user.is_admin:
            return redirect(url_for("admin_page"))
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
            _event, _comment = db.get_event(event_id=event_id)
            if _event is None or len(_event) == 0:
                abort(404)
            form = CommentForm()
            return render_template("event.html",
                                   form=form,
                                   event=_event,
                                   comments=_comment)
    elif request.method == "POST":
        if ('update' in request.form) and (not ('delete' in request.form)):
            update = request.form['update']
            comment_id = request.form['commentup']
            comment_update_query = """UPDATE comments SET content = %s WHERE id = %s; """
            with connection.cursor() as cursor:
                cursor.execute(comment_update_query, (update, comment_id))
                connection.commit()
            return redirect(
                url_for('event_page', club_id=club_id, event_id=event_id))

        if 'delete' in request.form:  #task=="delete"
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
                    connection.commit()
                    flash('Your comment has been posted')
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


@login_required
def add_announcement_page():
    """
    the admin interface for adding announcement
    """
    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    form = AnnouncementForm()
    if form.validate_on_submit():
        header = form.data["header"]
        content = form.data["content"]
        if 'image' in request.files:
            image = request.files['image'].read()
            binary_image = dbapi2.Binary(image)
        else:
            binary_image = ""
        ann = Announcement(header, content, binary_image)
        db = current_app.config["db"]
        db.add_announcement(ann, current_user.id)
        flash('announcement added to the database')
        return redirect(url_for("admin_page"))
    return render_template("ann_add.html", form=form)


@login_required
def edit_announcement_page(ann_id):
    """
    the admin interface for editing announcement
    """
    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    form = AnnouncementForm()
    db = current_app.config["db"]
    announcement = db.get_announcement(ann_id)
    img_update = True
    if form.validate_on_submit():
        header = form.data["header"]
        content = form.data["content"]
        if 'image' in request.files:
            if request.files['image'].filename == None or request.files[
                    'image'].filename == "":
                img_update = False
            image = request.files['image'].read()
            binary_image = dbapi2.Binary(image)
        else:
            binary_image = ""
        _announcement = Announcement(header=header,
                                     content=content,
                                     image=binary_image)
        db.update_announcement(ann_id=ann_id,
                               announcement=_announcement,
                               img_update=img_update)
        return redirect(url_for("admin_page"))
    form.header.data = announcement[2]
    form.content.data = announcement[3]
    form.image.data = announcement[4]
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT ENCODE(announcements.blob_image, 'base64') FROM announcements WHERE id = %s",
            (ann_id, ))
        img = cursor.fetchone()
        image = []
        image.append(img[0])
        image = "data:image/png;base64," + image[0]
    return render_template("ann_edit.html", form=form, img=image)


@login_required
def add_event_page():
    """
    the admin interface for adding event
    """
    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    form = EventForm()
    if form.validate_on_submit():
        header = form.data["header"]
        content = form.data["content"]
        date = form.data["date"]
        if 'image' in request.files:
            image = request.files['image'].read()
            binary_image = dbapi2.Binary(image)
        else:
            binary_image = ""
        event = Event(header=header,
                      content=content,
                      date=date,
                      image=binary_image)
        db = current_app.config["db"]
        db.add_event(event, current_user.id)
        flash('event added to the database')
        return redirect(url_for("admin_page"))
    return render_template("event_add.html", form=form)


@login_required
def edit_event_page(event_id):
    """
    the admin interface for editing event
    """
    if not current_user.is_authenticated:
        return redirect(url_for('admin_login'))
    if not current_user.is_admin:
        return redirect(url_for('admin_login'))
    try:
        form = EventForm()
        db = current_app.config["db"]
        event = db.get_event_info(event_id)
        img_update = True
        if form.validate_on_submit():
            header = form.data["header"]
            content = form.data["content"]
            date = form.data["date"]
            if 'image' in request.files:
                if request.files['image'].filename == None or request.files[
                        'image'].filename == "":
                    img_update = False
                image = request.files['image'].read()
                binary_image = dbapi2.Binary(image)
            else:
                binary_image = ""
            _event = Event(header=header,
                           content=content,
                           date=date,
                           image=binary_image)
            db.update_event(event_id=event_id,
                            event=_event,
                            img_update=img_update)
            return redirect(url_for("admin_page"))
        form.header.data = event[2]
        form.content.data = event[3]
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ENCODE(events.blob_image, 'base64') FROM events WHERE id = %s",
                (event_id, ))
            img = cursor.fetchone()
            image = []
            image.append(img[0])
            image = "data:image/png;base64," + image[0]
        return render_template("event_edit.html", form=form, img=image)
    except Exception as e:
        print(e)


@login_required
def profile(user_id):
    """
    a profile page for normal registered users
    if it is users own profile; user can change account info
    else; user can see the common clubs and basic information of the other user
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.is_admin:
        abort(401)
    try:
        form = UserUpdateForm()
        user = get_user_by_id(id=current_user.id)
        if request.method == 'GET':
            if user_id == current_user.id:
                user = get_user_by_id(id=current_user.id)
                form.name.data = user.name
                form.surname.data = user.surname
                form.student_id.data = user.student_id
                form.email.data = user.email
                #form.department.data = user.department
                if user.gender:
                    form.gender.data = user.gender
                return render_template('profile.html',
                                       form=form,
                                       name=None,
                                       surname=None,
                                       student_id=None,
                                       department=None)
            elif user_id != current_user.id:
                user = get_user_by_id(id=user_id)
                name = user.name
                surname = user.surname
                student_id = user.student_id
                department = user.department
                get_common_clubs_statement = """select clubs.id, clubs.name from clubs 
                                                join members 
                                                on clubs.id = members.club_id 
                                                join users 
                                                on users.id = members.user_id 
                                                where users.id = %s
                                                INTERSECT 
                                                select clubs.id, clubs.name from clubs 
                                                join members 
                                                on clubs.id = members.club_id 
                                                join users 
                                                on users.id = members.user_id 
                                                where users.id = %s """
                with connection.cursor() as cursor:
                    cursor.execute(get_common_clubs_statement,
                                   (current_user.id, user_id))
                    common_clubs = cursor.fetchall()

                return render_template('profile.html',
                                       name=name,
                                       surname=surname,
                                       student_id=student_id,
                                       department=department,
                                       common_clubs=common_clubs)
        elif request.method == 'POST':
            if 'delete' in request.form:
                return "asd"
                logout_user()
                delete_user(user_id=user_id)
                flash('User Deleted')
                return redirect(url_for('register'))
            if form.validate_on_submit():
                name = form.data["name"]
                surname = form.data["surname"]
                student_id = form.data["student_id"]
                email = form.data["email"]
                if form.data["gender"]:
                    gender = form.data["gender"]
                else:
                    gender = None
                x = False
                if (user.student_id != student_id):
                    x = True
                update_user(current_user.id, name, surname, student_id, email,
                            gender)
                if x:
                    flash(
                        'Your student id is changed, login again with your new id'
                    )
                return redirect(url_for('profile', user_id=current_user.id))
            else:
                print(form.errors)
                return render_template('profile.html', form=form)
    except Exception as e:
        print("Error in profile page", e)


@login_required
def club_update_page():
    """
    admin interface where admşns can update the info of club
    """
    if (not current_user.is_authenticated) or (current_user.is_admin == False):
        return redirect(url_for('admin_login'))
    club_id = 0
    club_name = ""
    with connection.cursor() as cursor:
        get_club_id = """select clubs.id as club_id , clubs.name  
        from clubs 
        join club_managers as cm 
        on cm.club_id = clubs.id 
        join club_admins as ca 
        on ca.id = cm.admin_id 
        WHERE ca.id = %(admin_id)s; """
        cursor.execute(get_club_id, {'admin_id': current_user.id})
        info = cursor.fetchone()
        club_id = info[0]
        club_name = info[1]
    form = ClubUpdateForm()
    db = current_app.config["db"]
    club = db.get_club(club_key=club_id)

    if form.validate_on_submit():
        description = form.data["description"]
        history = form.data["history"]
        source = form.data["source"]
        mission = form.data["mission"]
        vision = form.data["vision"]
        with connection.cursor() as cursor:
            st = """UPDATE clubs SET description = %(description)s, history = %(history)s, 
            source = %(source)s, mission = %(mission)s, vision = %(vision)s WHERE id = (select clubs.id as club_id  
        from clubs 
        join club_managers as cm 
        on cm.club_id = clubs.id 
        join club_admins as ca 
        on ca.id = cm.admin_id 
        WHERE ca.id = %(admin_id)s);"""
            data = {
                'description': description,
                'history': history,
                'source': source,
                'mission': mission,
                'vision': vision,
                'admin_id': current_user.id
            }
            cursor.execute(st, data)
            connection.commit()
            return redirect(url_for('club_update_page', club_id=club_id))
    form.description.data = club[2]
    form.history.data = club[3]
    form.source.data = club[5]
    form.mission.data = club[6]
    form.vision.data = club[7]
    return render_template('club_update.html',
                           form=form,
                           club_id=club_id,
                           club_name=club_name)


@login_required
def reach_others():
    """
    a page where a user can check out other registered users
    see which clubs they have in common
    """
    if (not current_user.is_authenticated) or (current_user.is_admin):
        return redirect(url_for('login'))
    try:
        with connection.cursor() as cursor:
            get_all_users_statement = """SELECT * FROM users"""
            cursor.execute(get_all_users_statement)
            all_users = cursor.fetchall()
            return render_template('reach_others.html', all_users=all_users)
    except Exception as e:
        print('Error while reaching others: ', e)