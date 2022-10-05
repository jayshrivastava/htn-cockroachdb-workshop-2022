import os
from pony.orm import Database, PrimaryKey, Required, sql_debug, db_session

pg_conn_string = os.environ["PG_CONN_STRING"]

db = Database()


class Book(db.Entity):
    _table_ = 'books'
    id = PrimaryKey(int, auto=True)
    title = Required(str, unique=True)
    author = Required(str)
    rating = Required(float)
    pages = Required(int)


db.bind('postgres', pg_conn_string)  # Bind Database object to the real database
# Create tables if they do not exist. Noop if they do exist
db.generate_mapping(create_tables=True)

@db_session
def create_books():
  # The database will assign ids for us.
  Book(id = 0, title="To Kill a Mockingbird", author="Harper Lee", rating=4.42, pages=281)
  Book(id = 1, title="George Orwell", author="George Orwell", rating=4.18, pages=387)
  Book(id = 2, title="Treasure Island", author="Robert Louis Stevenson", rating=3.83, pages=311)


@db_session
def get_book(id):
    # Use to_dict() to convert an object to a dictionary.
    book = Book.get(id=id).to_dict()
    print(book)


@db_session
def search_books(min_rating):
    books_query = Book.select(lambda book: book.rating >= min_rating)
    print([book.to_dict() for book in books_query])

@db_session
def update_author(id, new_author):
    book = Book.get(id=id)
    book.author = new_author

@db_session
def delete_book(id):
    book = Book.get(id=id)
    book.delete()
 

create_books()
get_book(0)
search_books(4)
update_author(1, "Me")
delete_book(1)

  
