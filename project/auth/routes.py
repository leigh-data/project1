from flask import Blueprint, render_template, redirect

from project.auth.forms import RegistrationForm
from project import db

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        books = db.session.execute("SELECT * FROM books").fetchall()[:3]
        return str(books)
    else:
        return render_template("auth/register.html", form=form)
