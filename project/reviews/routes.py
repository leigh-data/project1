from flask import Blueprint, render_template, redirect, flash, url_for, session, abort
from utils.decorators import login_required

from project.reviews.forms import ReviewForm, DeleteReviewForm
from project import db


reviews_blueprint = Blueprint('reviews', __name__)


@reviews_blueprint.route("/<string:isbn>/reviews", methods=['GET', 'POST'])
@login_required
def create_review(isbn):

    book_id = db.session.execute(
        "SELECT id FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()[0]
    user_id = session['user_id']

    has_review = db.session.execute(
        "SELECT COUNT(*) FROM reviews WHERE book_id=:book_id AND user_id=:user_id",
        {'book_id': book_id, 'user_id': user_id}).fetchone()[0]

    if book_id < 1:
        abort(404)

    if has_review > 0:
        flash("You have already left a review.")
        return redirect(url_for('books.detail', isbn=isbn))

    form = ReviewForm()

    if form.validate_on_submit():
        data = {
            'user_id': user_id,
            'comment': form.comment.data,
            'rating': form.rating.data,
            'book_id': book_id
        }

        db.session.execute(
            "INSERT INTO reviews (user_id, book_id, comment, rating) VALUES (:user_id, :book_id, :comment, :rating)", data)
        db.session.commit()

        flash("Comment has been added.")
        return redirect(url_for('books.detail', isbn=isbn))
    return render_template('reviews/create.html', form=form, isbn=isbn)


@reviews_blueprint.route("/<string:isbn>/reviews/update", methods=['GET', 'POST'])
@login_required
def update_review(isbn):
    try:
        book_id = db.session.execute(
            "SELECT id FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()[0]
        user_id = session['user_id']
        data = {'book_id': book_id, 'user_id': user_id}

        review = db.session.execute(
            "SELECT comment, rating FROM reviews WHERE book_id=:book_id AND user_id=:user_id",
            data).fetchone()

        if book_id is None:
            # abort(404)
            return "BOOK ID IS NONE"

        form = ReviewForm(obj=review)

        if form.validate_on_submit():
            rating = form.rating.data
            comment = form.comment.data

            data['rating'] = rating
            data['comment'] = comment

            db.session.execute(
                "UPDATE reviews SET comment=:comment, rating=:rating WHERE book_id=:book_id AND user_id=:user_id",
                data)
            db.session.commit()

            flash("Your review has been updated")
            return redirect(url_for('books.detail', isbn=isbn))

        return render_template('reviews/update.html', form=form, isbn=isbn)
    except:
        abort(404)


@reviews_blueprint.route("/<string:isbn>/reviews/delete", methods=['POST'])
@login_required
def delete_review(isbn):
    user_id = session['user_id']
    book_id = db.session.execute(
        "SELECT id FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()[0]
    data = {
        'user_id': user_id,
        'book_id': book_id
    }

    form = DeleteReviewForm()

    if form.validate_on_submit():
        db.session.execute("DELETE FROM reviews WHERE user_id=:user_id AND book_id=:book_id",
                           data)
        db.session.commit()

        flash("The review has been deleted.")

    else:
        flash("The review could not be deleted.")

    return redirect(url_for('books.detail', isbn=isbn))
