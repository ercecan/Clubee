import psycopg2

try:
    conn = psycopg2.connect(
        "dbname='test' user='postgres' host='localhost' password='95175305Ee'")
    print("ad")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

cur.execute("""SELECT * from test_t""")

rows = cur.fetchall()  ##we have the table in the variable

print("\nShow me the databases:\n")
for row in rows:
    print("   ", row[0], row[1])  ##acts like a matrix x rows, n columns
