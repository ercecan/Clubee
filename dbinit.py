import psycopg2 as dbapi2
from config import Config
import sys


def read_sql_from_file(filename):
    """
    reads all the lines in sql splitting with ';' character
    """
    with open(filename, 'r') as f:
        content = f.read()
        content = content.split(';')
        content = [row + ";" for row in content]
    return content


def initialize():
    """
    initializes the database
    """
    try:
        with dbapi2.connect(
                Config.db_url, sslmode='require'
        ) as connection:  ##### , sslmode='require' heroku için parametrelere ekle
            with connection.cursor() as cursor:
                print("Connected...")

                drop_statements = read_sql_from_file('drop.sql')
                for statement in drop_statements:
                    if len(statement) > 5:
                        cursor.execute(statement)
                        connection.commit()
                print("Drop tables...")

                create_statements = read_sql_from_file('database.sql')
                for statement in create_statements:
                    if len(statement) > 5:
                        cursor.execute(statement)
                        connection.commit()
                print("Create tables...", file=sys.stderr)

                insert_statements = read_sql_from_file('clubs.sql')
                for statement in insert_statements:
                    if len(statement) > 5:
                        cursor.execute(statement)
                        connection.comit()
                print("Inserting into clubs...", file=sys.stderr)

                admin_insert_statements = read_sql_from_file('admin.sql')
                for statement in admin_insert_statements:
                    if len(statement) > 5:
                        cursor.execute(statement)
                        connection.commit()
                print("Inserting into admins...", file=sys.stderr)

                areas_insert_statements = read_sql_from_file('areas.sql')
                for statement in areas_insert_statements:
                    if len(statement) > 5:
                        cursor.execute(statement)
                        connection.commit()
                print("Inserting areas...", file=sys.stderr)

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error))


if __name__ == "__main__":
    initialize()
"""
##Should I do commits ?? commit as in rollback / commit
cur = conn.cursor()
cur.execute(query_drop)
cur.execute(query_create)
conn.commit()
"""