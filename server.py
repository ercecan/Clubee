from flask import Flask, request, Response
from database import Database
from models import Club
import views
from config import Config
from flask_login import LoginManager
from user import get_user
from dbinit import initialize
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
# use env to load template(s)

lm = LoginManager()


@lm.user_loader
def load_user(
    user_id
):  ###### burdan if else falan ekleyip ekleyip başka fonksyionlar da kullanabilirsin!!!!
    return get_user(user_id)


def create_app():

    app = Flask(__name__)
    app.jinja_env.globals.update(
        zip=zip)  ####required to use 'zip' functionality in jinja
    ####app = bilmem ne bilmem ne burda vercen
    app.config.from_object(Config)
    #app.config.from_object("settings")
    #initialize()  ##heroku için commenti kaldır
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/index", view_func=views.home_page)
    app.add_url_rule("/home", view_func=views.home_page)
    app.add_url_rule("/clubs", view_func=views.clubs_page)
    app.add_url_rule("/myclubs", view_func=views.myclubs_page)
    app.add_url_rule("/announcements",
                     view_func=views.announcements_page,
                     methods=["GET"])
    app.add_url_rule("/clubs/<int:club_id>", view_func=views.club_page)
    app.add_url_rule("/login", view_func=views.login, methods=["GET", "POST"])
    app.add_url_rule("/logout",
                     view_func=views.logout,
                     methods=["GET", "POST"])
    app.add_url_rule("/adminlogin",
                     view_func=views.admin_login,
                     methods=["POST", "GET"])
    app.add_url_rule("/adminlogout",
                     view_func=views.admin_logout,
                     methods=["POST"])
    app.add_url_rule("/adminpage",
                     view_func=views.admin_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/register",
                     view_func=views.register,
                     methods=["GET", "POST"])
    app.add_url_rule("/clubs/<int:club_id>/leave",
                     view_func=views.leave_club,
                     methods=["POST"])
    app.add_url_rule("/clubs/<int:club_id>/join",
                     view_func=views.join_club,
                     methods=["POST"])
    app.add_url_rule("/clubs/<int:club_id>/announcements/<int:ann_id>",
                     view_func=views.announcement_page,
                     methods=["GET"])
    app.add_url_rule("/clubs/<int:club_id>/events/<int:event_id>",
                     view_func=views.event_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/adminpage/addannouncement",
                     view_func=views.add_announcement_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/adminpage/editannouncement/<int:ann_id>",
                     view_func=views.edit_announcement_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/adminpage/addevent",
                     view_func=views.add_event_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/adminpage/editevent/<int:event_id>",
                     view_func=views.edit_event_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/profile/<int:user_id>",
                     view_func=views.profile,
                     methods=["GET", "POST"])
    app.add_url_rule("/adminpage/updateclub",
                     view_func=views.club_update_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/reach-others",
                     view_func=views.reach_others,
                     methods=["GET"])
    # app.add_url_rule("/asd",
    #                  view_func=views.upload_file,
    #                  methods=['GET', 'POST'])

    lm.init_app(app)
    lm.login_view = "admin_login"
    """
    lm.blueprint_login_views = {
        'login': '/login',
        'admin_login': '/adminlogin'
    }
    """

    db = Database()

    app.config["db"] = db
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)