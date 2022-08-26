import os
import psycopg2

user = os.environ["USERNAME"]
host = os.environ['HOST']
cluster = os.environ["CLUSTER"]
password = os.environ["DATABASE_PW"]

# Test Psycopg2
conn = psycopg2.connect(user=user,
                 host=host,
                 port=26257,
                 database=f'{cluster}.defaultdb',
                 password=password, sslmode='verify-full')
with conn.cursor() as cur:
    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)

# Test PonyORM
from pony.orm import Database, db_session

db = Database()
db_params = dict(provider='cockroach',
                 user=user,
                 host=host,
                 port=26257,
                 database=f'{cluster}.defaultdb',
                 password=password)

db.bind(**db_params)  # Bind Database object to the real database

@db_session
def test():
    res = db.select('SELECT now()')
    print(res)
test()
