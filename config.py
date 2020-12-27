import os

dsn = """dbname='Clubee' user='postgres'
         host='localhost' password='95175305Ee'"""


class Config(object):
    SECRET_KEY = "b'\xaeLI\xd1z\xe6wI\x8b\xdd\r\xc5\xfeA+\xa0K\x04\xa4\x12\xfdW\x11\xf9'"  # os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    PORT = 8080
    db_url = dsn