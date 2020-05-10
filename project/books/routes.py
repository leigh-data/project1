from flask import Blueprint

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route("/")
def index():

    return "HELLO BOOKS"
