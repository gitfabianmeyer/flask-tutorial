import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    #g is object unique f.e request to store data
    if 'db' not in g:
        # connect establishes connection to file ponted bei DATABSE config key
        g.db = sqlite3.connect(
            # use current app because application calls get_db, so app is created
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells connection to return rows that behave like dicts. Allows
        # accessing columns by name
        g.db.row_factory=sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    #returns database connection
    db = get_db()
    #opens file relative to flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new table"""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    """close_db and init_db_command need to be reqistered with app instance. As we use a factory, instance
    is not available when writing this. init_app takes app and does registration"""

    # tells flask to call close_db when cleanung up after response
    app.teardown_appcontext(close_db)
    #add new command to be called with "flask" command
    app.cli.add_command(init_db_command)