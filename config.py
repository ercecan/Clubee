import os

# h_url = os.environ.get("DATABASE_URL")  #for heroku
# dsn = h_url  #for heroku
dsn = """dbname='Clubee' user='postgres'
         host='localhost' password='95175305Ee'"""


class Config(object):
    SECRET_KEY = "b'\xaeLI\xd1z\xe6wI\x8b\xdd\r\xc5\xfeA+\xa0K\x04\xa4\x12\xfdW\x11\xf9'"  # os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    PORT = 8080
    db_url = dsn
    PASSWORDS = {
        "123456789":
        '$pbkdf2-sha256$29000$kVKKESIEIIQQwpgzptRaaw$tc/vVEpEjE50VNGAUtkT5oiXOEjOVtCP17wHGm9zgHI'
    }
    ADMIN_PASSWORDS = {
        "erce":
        '$pbkdf2-sha256$29000$gXDOeY.xlvL.H4Pw3hsDIA$izC3DlUcd4jLAXj4i.cZfv4ejyCUXHiYrONUTBXrXFQ'
    }

    USERS = ["123456789"]
    ADMIN_USERS = ["erce"]
    UPLOAD_FOLDER = '/stattic/images'