# Part 2
from flask import Flask, jsonify, request
# Part 4
import json
# Part 6
import os
# Part 7
import random
from pony.orm import Database, PrimaryKey, Required, sql_debug, db_session

# Create a Flask server.
app = Flask(__name__)

"""
Part 7 - Working with A Database
"""
# Source: https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-pony.html
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
# db_params = dict(provider='cockroach', user='jayant', host='free-tier.gcp-us-central1.cockroachlabs.cloud', port=26257, database='ample-lemur-3072.defaultdb', os.getenv('db_password'))
# Note: You will need to set the db_password environment variable in repl.it (see https://docs.replit.com/tutorials/08-storing-secrets-and-history). 

sql_debug(True)  # Print all generated SQL queries to stdout
db.bind(**db_params)  # Bind Database object to the real database
db.generate_mapping(create_tables=True)  # Create tables

# Helper functions!
@db_session  # db_session decorator manages the transactions
def db_create_book(title, author, rating, pages):
  return Book(title=title, author=author, rating=rating, pages=pages).to_dict()

@db_session
def db_get_all_books():
  return [book.to_dict() for book in Book.select()]

@db_session 
def db_get_book(title, author, rating, pages):
  return Book(title, author, rating, pages).to_dict() 

@db_session 
def db_filter_books(max_pages, min_rating):
  if not max_pages:
    max_pages = float('inf')
  if not min_rating:
    min_rating = float('-inf')
  books_query = Book.select(lambda book: book.rating >= min_rating and book.pages <= max_pages)
  return [book.to_dict() for book in books_query]

@db_session
def db_change_author(id, new_author):
  book = Book.get(id=id)
  book.author = new_author 
  return book.to_dict()

@db_session
def db_delete_book(id):
  book = Book.get(id=id)
  book_dict = book.to_dict()
  book.delete()
  return book_dict

# Routes!
@app.route('/', methods=['GET'])
def index():
    return jsonify(db_get_all_books())

@app.route("/<id>", methods=['GET'])
@db_session
def get_book(id):
  book = Book.get(id=id)
  if not book:
     return jsonify({"error": "invalid id"})
  return jsonify(Book.get(id=id).to_dict())

@app.route("/search", methods=['GET'])
def search_books():
  result = db_filter_books(int(request.args.get('max_pages')), int(request.args.get('min_rating')))
  return jsonify(result)

@app.route("/", methods=['POST'])
def create_book():
  new_book = request.json
  try:
    db_create_book(new_book['title'], new_book['author'], new_book['rating'], new_book['pages'])
  except:
    return jsonify({"error": "could not create this book"})
  return jsonify(new_book)

@app.route("/<id>", methods=['PUT'])
def update_author(id):
  try:
    author = request.json['author']
    return jsonify(db_change_author(id, author))
  except:
    return jsonify({"error": "could not update book"})

@app.route("/<id>", methods=['DELETE'])
def delete_book(id):
  try:
    return jsonify(db_delete_book(id))
  except:
    return jsonify({"error": "could not delete book"})

"""
End of Part 7 Code
"""

"""
Parts 2-5 - Building an API without a Database
"""

# # Books stored in memory in a Python dictionary
# books = {
#   0: {'id': 0,
#     'title': 'Harry Potter and the Chamber of Secrets (Harry Potter #2)',
#     'author': 'J.K. Rowling',
#     'rating': 4.42,
#     'pages': 352},
#   1: {'id': 1,
#     'title': 'The Fellowship of the Ring (The Lord of the Rings #1)',
#     'author': 'J.R.R. Tolkien',
#     'rating': 4.36,
#     'pages': 398},
#   2: {'id': 2,
#     'title': 'Treasure Island',
#     'author': 'Robert Louis Stevenson',
#     'rating': 3.83,
#     'pages': 311}
# }

# # Part 3 - Get Requests
# @app.route('/', methods=['GET'])
# def index():
#     return jsonify([books[book_id] for book_id in books])

# # Request Params Example
# @app.route("/<id>", methods=['GET'])
# def get_book(id):
#     if int(id) not in books:
#       return jsonify({"error": "invalid id"})
#     return jsonify(books[int(id)])

# # Route Params Example
# @app.route("/search", methods=['GET'])
# def search_books():
#   result = []

#   for book_id, book in books.items():
#     if request.args.get('max_pages'):
#       if book['pages'] > int(request.args.get('max_pages')):
#         continue

#     if request.args.get('min_rating'):
#       if book['rating'] < int(request.args.get('min_rating')):
#         continue

#     result.append(book)
#   return jsonify(result)

# # Part 4 - Post Requests
# @app.route("/", methods=['POST'])
# def create_book():
#   new_book = request.json
#   if new_book['id'] in books:
#     return jsonify({"error": "book with that id already exists"})

#   books[new_book['id']] = new_book
#   return jsonify(new_book)

# # Part 5 - Put and Delete Requests
# @app.route("/<id>", methods=['PUT'])
# def update_author(id):
#   if int(id) not in books:
#     return jsonify({"error": "invalid id"})
#   books[int(id)]['author'] = request.json['author']

#   return jsonify(books[int(id)])

# @app.route("/<id>", methods=['DELETE'])
# def delete_book(id):
#   if int(id) not in books:
#     return jsonify({"error": "invalid id"})
#   deleted_book = books[int(id)]
#   del books[int(id)]
#   return jsonify(deleted_book)

"""
End of Parts 2-5
"""

# Runs the API and exposes it on https://<repl name>.<replit username>.repl.co
# ex. Mine deploys to https://htn-api.jayantsh.repl.co.
app.run(
  host = "0.0.0.0",
  debug = True
)




