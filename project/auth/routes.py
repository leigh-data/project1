from flask import Blueprint, render_template, redirect, flash, url_for

from project.auth.forms import RegistrationForm
from project import db, bcrypt

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        data = {
            'username': form.username.data,
            'password': bcrypt.generate_password_hash(form.password.data)
        }

        db.session.execute("INSERT INTO users(username, password) VALUES (:username, :password)",
                           data)
        db.session.commit()
        flash("You are now registered.")
        return redirect(url_for("books.index"))
    else:
        return render_template("auth/register.html", form=form)
