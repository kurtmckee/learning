import os
import random
import urllib.parse

import flask
import requests


app = flask.Flask(__name__.split(".")[0])


CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")
AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_INFO_ENDPOINT = "https://api.github.com/user"

if not CLIENT_ID:
    raise EnvironmentError("GITHUB_CLIENT_ID must be a valid environment variable")
if not CLIENT_SECRET:
    raise EnvironmentError(f"GITHUB_CLIENT_SECRET must be a valid environment variable")


@app.route("/")
def home():
    return (
        '<a href="http://127.0.0.1:5000/login">Login</a>'
        "<br>"
        '<a href="http://127.0.0.1:5000/logout">Logout</a>'
        "<br>"
        '<a href="http://127.0.0.1:5000/user">Display GitHub user info</a>'
    )


@app.route("/callback")
def callback():
    if flask.session.get("access_token"):
        return flask.redirect("/user")
    if flask.request.args.get("state") != flask.session.get("state"):
        return "Incorrect state"
    if not flask.request.args.get("code"):
        return "No code"

    headers = {
        "ACCEPT": "application/vnd.github.v3+json, application/json",
        "USER-AGENT": "https://none.invalid/",
    }

    parameters = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:5000/callback",
        "code": flask.request.args["code"],
    }

    response = requests.post(
        url=TOKEN_URL,
        headers=headers,
        params=parameters,
    )
    flask.session["access_token"] = response.json()["access_token"]

    return flask.redirect("/user")


@app.get("/user")
def display_user_info():
    if not flask.session.get("access_token"):
        return flask.redirect('/login')

    response = requests.get(
        url=USER_INFO_ENDPOINT,
        headers={
            "AUTHORIZATION": f'token {flask.session["access_token"]}',
            "ACCEPT": "application/vnd.github.v3+json",
        },
    )

    return (
        f'<a href="{response.json()["html_url"]}">github.com/{response.json()["login"]}</a>'
        "<br>"
        '<a href="http://127.0.0.1:5000/logout">Logout</a>'
    )


@app.route("/login")
def login():
    if flask.session.get("access_token"):
        return flask.redirect("/user")

    flask.session["state"] = "".join(
        [chr(random.randrange(ord("a"), ord("z") + 1)) for _ in range(10)]
    )
    parameters = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:5000/callback",
        "scope": "read:user",
        "state": flask.session["state"],
    }
    url = AUTHORIZE_URL + "?" + urllib.parse.urlencode(parameters)
    return f'<a href="{url}">Click here to login</a>'


@app.route("/logout")
def logout():
    if flask.session.get("access_token"):
        flask.session.pop("access_token")
        return (
            "You have been logged out."
            "<br>"
            '<a href="http://127.0.0.1:5000/login">Click here to login</a>.'
        )

    return (
        "You are not currently logged in."
        "<br>"
        '<a href="http://127.0.0.1:5000/login">Click here to login</a>.'
    )


app.secret_key = "secret-squirrel"
app.run()
