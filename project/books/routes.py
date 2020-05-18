from flask import Blueprint, render_template, session, abort, request, redirect, url_for, flash
from project import db
from utils.decorators import login_required
from project.ratings.forms import DeleteRatingForm

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route("/")
def index():
    books = db.session.execute(
        "SELECT id, isbn, title, author, year FROM books").fetchall()
    return render_template('books/index.html', books=books)


@books_blueprint.route("/search", methods=['GET'])
@login_required
def search():
    query = request.args.get('q')
    if not query:
        flash("You must enter a search string.")
        return redirect(url_for('books.index'))

    page = request.args.get('page')
    page = int(page)

    page_count = db.session.execute("""
    SELECT CEILING(CAST(COUNT(*) AS DECIMAL)/5) FROM books WHERE tsv @@ plainto_tsquery(:query);
    """, {'query': query}).fetchone()[0]

    if page_count == 0:
        return abort(404)

    if page > page_count:
        page = page_count

    has_next = page < page_count
    has_previous = page > 1

    books = db.session.execute("""
    SELECT id, author, title, isbn                                                                                                                                  
    FROM books                                                                                                                                                                 
    WHERE tsv @@ plainto_tsquery(:query)                                                                                                                                   
    ORDER BY id ASC                                                                                                                                                            
    LIMIT :page_size offset ((:page - 1) * :page_size)
    """, {'query': query, 'page': page, 'page_size': 5}).fetchall()

    return render_template('books/search.html',
                           books=books,
                           page=page,
                           query=query,
                           has_next=has_next,
                           has_previous=has_previous)


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
