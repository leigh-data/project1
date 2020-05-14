from flask import Blueprint, render_template, redirect, flash, url_for, session
from utils.decorators import login_required


comment_blueprint = Blueprint('comments', __name__)


@comment_blueprint.route("/<string:isbn>/comment", methods=['GET', 'POST'])
@login_required
def create_comment(isbn):
    return f"COMMENT:{isbn}"


@comment_blueprint.route("/<string:isbn>/comment/update", methods=['GET', 'POST'])
@login_required
def update_comment(isbn):
    return f"COMMENT UPDATE:{isbn}"


@comment_blueprint.route("/<string:isbn>/comment/delete", methods=['GET', 'POST'])
@login_required
def delete_comment(isbn):
    return f"DELETE UPDATE:{isbn}"
