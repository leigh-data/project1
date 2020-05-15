from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None and session.get('user_id'):
            flash('Please login to continue', 'warning')
            return redirect(url_for('books.index'))
        return f(*args, **kwargs)
    return decorated_function
