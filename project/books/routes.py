from flask import Blueprint, render_template, session, abort
from project import db
from project.ratings.forms import DeleteRatingForm

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route("/")
def index():
    books = db.session.execute(
        "SELECT id, isbn, title, author, year FROM books").fetchall()
    return render_template('books/index.html', books=books)


@books_blueprint.route("/<isbn>")
def detail(isbn):
    book = db.session.execute(
        "SELECT id, isbn, title, author, year FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()

    if book is not None:
        data = {'book_id': book.id}

        ratings = db.session.execute("""
        SELECT users.username, ratings.rating, ratings.comment
        FROM ratings
        JOIN users on users.id=ratings.user_id
        WHERE ratings.book_id=:book_id
        """, data).fetchall()

        has_rating = db.session.execute(
            "SELECT COUNT(*) FROM ratings WHERE book_id=:book_id AND user_id=:user_id",
            {'book_id': book['id'], 'user_id': session['user_id']}).fetchone()[0] > 0

        if has_rating:
            form = DeleteRatingForm()
        else:
            form = None

        return render_template('books/detail.html', book=book, has_rating=has_rating, ratings=ratings, form=form)
    else:
        abort(404)
