from flask import Blueprint, render_template
from project import db

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route("/")
def index():
    books = db.session.execute(
        "SELECT id, isbn, title, author, year FROM books").fetchall()
    return render_template('books/index.html', books=books)


@books_blueprint.route("/<isbn>")
def detail(isbn):
    books = db.session.execute(
        "SELECT id, isbn, title, author, year FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchall()
    return render_template('books/detail.html', books=books)
