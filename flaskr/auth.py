import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# creates a Blueprint named 'auth'
# __name__ gives local context, prefix will prepeded to all urls associated with the bp
bp = Blueprint('auth', __name__, url_prefix='/auth')

#connects function with url
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        #validate not empty pass/usern
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        #use db execute to be invulnerable to sql injection attack
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                #use password hash
                'INSERT INTO user (username, password) VALUES (?,?)',
                (username, generate_password_hash(password))
            )
            #commit to save modifications
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',(username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is dict that stores data across requests. Data is stored in cookie and
            # than send into browser
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

# runs before view function, on every url.
# load_logged.. stores user id on g.user, which lasts for length of request
@bp.before_app_first_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#to logout: remove user id from session
@bp.route('\logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#wraps new view function around original view its applied to
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        #check user
        if g.user is None:
            #redicrect to login page
            return redirect(url_for('auth.login'))
        # otherwise return original view
        return view(**kwargs)
    return wrapped_view



