import sqlite3
import typing as t

import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext


def get_db():
    """Open and return a connection to the database.

    The connection is cached in Flask's `g` object.
    https://flask.palletsprojects.com/en/2.0.x/appcontext/
    """

    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error: t.Optional[BaseException] = None):
    """Close the database connection, if any.

    The Flask tutorial doesn't mention this, but mypy pointed out that
    functions called by `teardown_appcontext()` must accept a possible
    exception argument.

    https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.teardown_appcontext
    """

    db = g.get("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database."""

    db = get_db()

    # `.open_resource()` will open the SQL file relative to the root path,
    # NOT relative to the instance folder.
    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Erase existing data and create new tables."""

    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask):
    """Add database-related init and teardown functions to the Flask app.

    This method must be imported and called from with `create_app()`.
    """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
