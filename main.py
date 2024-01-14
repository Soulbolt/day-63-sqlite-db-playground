import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# db = sqlite3.connect("books-collection.db")

# cursor = db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

app = Flask(__name__)

# Database
class Base(DeclarativeBase):
    pass

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# Extension
db = SQLAlchemy(model_class=Base)

# Initialize the app with the extension
db.init_app(app)
# Define Model
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    review: Mapped[float] = mapped_column(Float, nullable=False)
# Create the table schema in the database, Requires application context
# with app.app_context():
#     db.create_all()

# CRUD queries below
# Create record
with app.app_context():
    new_book= Book(id=1, title="Harry Potter", author="J.K. Rowling", review=9.3)
    db.session.add(new_book)
    db.session.commit()
    
# Read all records query
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
# Read single record query
with app.app_context():
    book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()

# Update a record query
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    book_to_update.title = "Harry Potter and The Chamber of Secrets"
    db.session.commit()
    
# Update a record by primary key
book_id = 1
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_update = db,get_or_404(Book, book_id)
    book_to_update.title = "Harry Potter and The Goblet of Fire"
    db.session.commit()
    
# Delete a record by primary key
with app.app_context():
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_delete - db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
