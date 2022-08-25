OAuth2 native apps
******************


Goal
====

*   Follow the `Globus Auth docs`_ for native apps.
*   Use the `Globus SDK`_ to do a native app authorization.
*   Look at the object returned at each stage of the native app authorization flow.


Lessons learned
===============

*   The Globus SDK does a lot of heavy lifting!
*   For native apps, only a client ID is required.
    It looks like this could be published in an open source application.

    (For example, it looks like the Globus CLI does exactly this,
    though it also appears to create a confidential client application locally
    using its native app credentials.)

..  _Globus Auth docs: https://docs.globus.org/api/auth/developer-guide/
..  _Globus SDK: https://github.com/globus/globus-sdk-python/
