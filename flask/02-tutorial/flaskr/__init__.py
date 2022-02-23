import os
import typing as t

from flask import Flask


def create_app(test_config: t.Optional[t.Dict[str, t.Any]] = None):
    """Create and return a Flask app with a "/hello" route."""

    # `instance_relative_config` means that config.from_* methods will
    # try to find files with relative paths in the instance folder.
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # This will create an instance folder outside the "flaskr/" directory.
    # Should the instance folder be added to .gitignore?
    # https://flask.palletsprojects.com/en/2.0.x/config/#instance-folders
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello world!"

    return app
