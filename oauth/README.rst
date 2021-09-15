This is an attempt to learn more about `OAuth`_.

OAuth is a standard for *authorization*.
When coupled with OpenID Connect it can be used for *authentication*.

..  _OAuth: https://www.oauth.com/

To use this small app you will need an account on GitHub,
and you will need to register an OAuth application:

*   https://github.com/settings/developers
*   Click "Register a new application"
*   Enter this mandatory info, everything else doesn't matter:

    *   Homepage URL: https://none.invalid/
    *   Application callback URL: http://127.0.0.1:5000/callback

*   Click "Generate a new client secret"
*   In the shell where you'll launch this Flask app,
    set the following environment variables:

    *   GITHUB_CLIENT_ID
    *   GITHUB_CLIENT_SECRET

*   Launch the Flask app with:

    *   ``python server.py``

*   Visit http://127.0.0.1:5000/
