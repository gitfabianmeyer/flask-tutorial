import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# creates a Blueprint named 'auth'
# __name__ gives local context, prefix will prepeded to all urls associated with the bp
bp = Blueprint('auth', __name__, url_prefix='/auth')

