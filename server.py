from flask import Flask
from database import Database
from models import Club
import views
from config import Config
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    ####app = bilmem ne bilmem ne burda vercen
    app.config.from_object(Config)
    #app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/index", view_func=views.home_page)
    app.add_url_rule("/home", view_func=views.home_page)
    app.add_url_rule("/clubs", view_func=views.clubs_page)
    app.add_url_rule("/clubs/announcements", view_func=views.anns_page)
    app.add_url_rule("/clubs/<int:club_key>", view_func=views.club_page)
    app.add_url_rule("/login", view_func=views.login, methods=["GET", "POST"])
    app.add_url_rule("/admin-login",
                     view_func=views.admin_login,
                     methods=["GET", "POST"])

    db = Database()
    """
    db.add_club(
        Club("ITU ACM",
             description="singing",
             history="asd",
             announcements=["announcement1", "announcement2"],
             events=["event1", "event2"],
             vision="vision",
             mission="mission",
             student_count=2,
             image_url="../static/images/itu_acm.png"))

    db.add_club(
        Club("ITU IEEE",
             description="IEEE",
             history="old",
             announcements=["IEEEannouncement1", "IEEEannouncement2"],
             events=["IEEEevent1", "IEEEevent2"],
             vision="IEEEvision",
             mission="IEEEmission",
             student_count=2,
             image_url="../static/images/itu_ieee.png"))
    """
    app.config["db"] = db
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)