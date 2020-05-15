from flask import Blueprint, render_template, redirect, flash, url_for, session, abort
from utils.decorators import login_required

from project.ratings.forms import RatingForm
from project import db


ratings_blueprint = Blueprint('ratings', __name__)


@ratings_blueprint.route("/<string:isbn>/ratings", methods=['GET', 'POST'])
@login_required
def create_rating(isbn):

    book_id = db.session.execute(
        "SELECT id FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()[0]
    user_id = session['user_id']

    has_rating = db.session.execute(
        "SELECT COUNT(*) FROM ratings WHERE book_id=:book_id AND user_id=:user_id",
        {'book_id': book_id, 'user_id': user_id}).fetchone()[0]

    if book_id < 1:
        abort(404)

    if has_rating > 0:
        flash("You have already left a rating.")
        return redirect(url_for('books.detail', isbn=isbn))

    form = RatingForm()

    if form.validate_on_submit():
        data = {
            'user_id': user_id,
            'comment': form.comment.data,
            'rating': form.rating.data,
            'book_id': book_id
        }

        db.session.execute(
            "INSERT INTO ratings (user_id, book_id, comment, rating) VALUES (:user_id, :book_id, :comment, :rating)", data)
        db.session.commit()

        flash("Comment has been added.")
        return redirect(url_for('books.detail', isbn=isbn))
    return render_template('ratings/create.html', form=form, isbn=isbn)


@ratings_blueprint.route("/<string:isbn>/ratings/update", methods=['GET', 'POST'])
@login_required
def update_rating(isbn):
    # try:
    book_id = db.session.execute(
        "SELECT id FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()[0]
    user_id = session['user_id']
    data = {'book_id': book_id, 'user_id': user_id}

    rating = db.session.execute(
        "SELECT comment, rating FROM ratings WHERE book_id=:book_id AND user_id=:user_id",
        data).fetchone()

    form = RatingForm(obj=rating)

    if form.validate_on_submit():
        rating = form.rating.data
        comment = form.comment.data

        data['rating'] = rating
        data['comment'] = comment

        db.session.execute(
            "UPDATE ratings SET comment=:comment, rating=:rating WHERE book_id=:book_id AND user_id=:user_id",
            data)
        db.session.commit()

        flash("Your rating has been updated")
        return redirect(url_for('books.detail', isbn=isbn))

    return render_template('ratings/update.html', form=form, isbn=isbn)
    # except TypeError:
    #     flash('The book does not exist.')
    #     return redirect(url_for('books.index'))


@ratings_blueprint.route("/<string:isbn>/ratings/delete", methods=['GET', 'POST'])
@login_required
def delete_rating(isbn):
    return f"DELETE RATING:{isbn}"
