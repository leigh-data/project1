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
        "SELECT isbn, title, author, year FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()

    if book:

        return jsonify(dict(book))

    else:
        abort(404)
