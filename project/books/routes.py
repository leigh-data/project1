import requests
from flask import Blueprint, render_template, session, abort, request, redirect, url_for, flash, current_app
from project import db
from utils.decorators import login_required
from project.reviews.forms import DeleteReviewForm

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
@login_required
def detail(isbn):
    try:
        goodreads_key = current_app.config['GOODREADS_KEY']
        goodreads_response = requests.get(
            'https://www.goodreads.com/book/review_counts.json',
            params={'key': goodreads_key,
                    'isbns': isbn})

        goodreads_data = dict(goodreads_response.json())['books'][0]

    except:
        abort(404)

    book = db.session.execute(
        "SELECT id, isbn, title, author, year FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()

    if book is not None:
        data = {'book_id': book.id}

        reviews = db.session.execute("""
        SELECT users.username, reviews.rating, reviews.comment
        FROM reviews
        JOIN users on users.id=reviews.user_id
        WHERE reviews.book_id=:book_id
        """, data).fetchall()

        has_review = db.session.execute(
            "SELECT COUNT(*) FROM reviews WHERE book_id=:book_id AND user_id=:user_id",
            {'book_id': book['id'], 'user_id': session['user_id']}).fetchone()[0] > 0

        if has_review:
            form = DeleteReviewForm()
        else:
            form = None

        return render_template('books/detail.html', book=book, has_review=has_review, reviews=reviews, form=form, goodreads_data=goodreads_data)
    else:
        abort(404)
