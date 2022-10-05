import os
import psycopg2

pg_conn_string = os.environ["PG_CONN_STRING"]

# Test Psycopg2
conn = psycopg2.connect(pg_conn_string)
with conn.cursor() as cur:
  cur.execute("SELECT now()")
  res = cur.fetchall()
  conn.commit()
  print(res)

# Test PonyORM
from pony.orm import Database, db_session

db = Database()

db.bind('postgres',
        pg_conn_string)  # Bind Database object to the real database


@db_session
def test():
  res = db.select('SELECT now()')
  print(res)


test()
