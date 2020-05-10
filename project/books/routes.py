from flask import Blueprint, render_template

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route("/")
def index():

    return render_template('books/index.html', message="Hello!")
