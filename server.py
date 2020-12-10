from flask import Flask
from database import Database
from models import Club
import views
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/home", view_func=views.home_page)
    app.add_url_rule("/clubs", view_func=views.clubs_page)
    app.add_url_rule("/clubs/announcements", view_func=views.anns_page)
    app.add_url_rule("/clubs/<name>", view_func=views.club_page)
    app.add_url_rule("/login", view_func=views.login)

    db = Database()
    db.add_club(Club("Acapella", description="singing"))
    db.add_club(Club("quidditch"))
    app.config["db"] = db
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)