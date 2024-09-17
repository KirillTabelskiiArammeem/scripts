# pip3 install tabulate
import atexit
import datetime
import os
import psycopg2
from tabulate import tabulate
import time

host = os.getenv('DB_HOST_RO')
# host = os.getenv('DB_HOST_RW')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=host)


cur = conn.cursor()

atexit.register(lambda: (cur.close(), conn.close()))

while True:
    SESSIONS = 'SELECT * FROM pg_stat_activity;'
    cur.execute(SESSIONS)
    sessions = cur.fetchall()
    conn.commit()
    print("\n"*20)
    print(datetime.datetime.now())
    print(tabulate(sessions, headers=[desc[0] for desc in cur.description]))
    time.sleep(60)




cur.close()
conn.close()
