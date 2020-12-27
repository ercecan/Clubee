import psycopg2 as dbapi2

dsn = """dbname='test' user='postgres'
         host='localhost' password='95175305Ee'"""

try:
    conn = psycopg2.connect(dsn)
except Exception as e:
    print(e, "   Unable to reacn the database")
"""
###drop if exists and creat table
query_drop = "DROP TABLE IF EXISTS clubs CASCADE;"
query_create = "CREATE TABLE clubs (club_id SERIAL PRIMARY KEY,name VARCHAR(100) UNIQUE NOT NULL, description TEXT,history TEXT,student_count INTEGER DEFAULT 0, mission TEXT,vision TEXT,image_url TEXT);"

cur = conn.cursor()
cur.execute(query_drop)
cur.execute(query_create)
conn.commit()
"""
"""

###insertion into table
cur = conn.cursor()
query_insert = "INSERT INTO clubs (name,description,history,student_count,mission,vision,image_url) VALUES ('ITU ACM','description', 'history',12,'mission','vision','../static/images/itu_acm.png');"
query_insert2 = "INSERT INTO clubs (name,description,history,student_count,mission,vision,image_url) VALUES ('ITU IEEE','description', 'history',12,'mission','vision','../static/images/itu_acm.png');"
cur.execute(query_insert)
cur.execute(query_insert2)
conn.commit()
"""

cur = conn.cursor()
query_select = "SELECT * FROM clubs"
cur.execute(query_select)
rows = cur.fetchall()  ##we have the table in the variable

print("\nShow me the databases:\n")
#for row in rows:
print("   ", rows[0][1], rows[1][1])  ##acts like a matrix x rows, n columns
