from flask import Blueprint, jsonify, abort
from project import db

api_blueprint = Blueprint('api', __name__, url_prefix="/api")


@api_blueprint.errorhandler(404)
def not_found(error=None):
    data = {
        'status': 404,
        'message': 'Book not found.'
    }

    resp = jsonify(data)
    resp.status_code = 404

    return resp


@api_blueprint.route("/<isbn>", methods=['GET'])
def detail(isbn):
    book = db.session.execute(
        """SELECT books.isbn, books.title, books.author, books.year, 
            COUNT(reviews.rating) AS review_count, AVG(reviews.rating) AS average_score
            FROM books INNER JOIN reviews
            ON books.id=reviews.book_id
            WHERE books.isbn=:isbn
            GROUP BY books.id""", {'isbn': isbn}).fetchone()

    if book:
        data = {
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'review_count': book.review_count,
            'average_score': float(book.average_score)
        }
        return jsonify(data)

    else:
        abort(404)
