import random
import os
from pony.orm import Database, PrimaryKey, Required, sql_debug, db_session

db = Database()

class Book(db.Entity):
  _table_ = 'books'
  id = PrimaryKey(int,auto=True)
  title = Required(str,unique=True)
  author = Required(str)
  rating = Required(float)
  pages = Required(int)

# SQLite
# Store data in a file!
db_params = dict(provider='sqlite', filename='booksdb.sqlite', create_db=True) # The create_db option will create the file if it does not exist.

# CockroachDB 
# https://www.cockroachlabs.com/free-tier/
# db_params = dict(provider='cockroach', user='jayant', host='free-tier.gcp-us-central1.cockroachlabs.cloud', port=26257, database='scaly-deer-3088.defaultdb', password=os.getenv('db_password'))
# Note: You will need to set the db_password environment variable in repl.it (see https://docs.replit.com/tutorials/08-storing-secrets-and-history). 

sql_debug(True)  # Print all generated SQL queries to stdout
db.bind(**db_params)  # Bind Database object to the real database
db.generate_mapping(create_tables=True)  # Create tables

@db_session
def create_book(title, author, rating, pages):
  # the db will assign ids for us
  Book(title=title, author=author, rating=rating, pages=pages)

# Read CSV Data and Create Books
f = open("books.csv", "r")
for line in f:
  parts = line.strip().split(',')
  create_book(parts[1], parts[2], float(parts[3]), parts[4])
