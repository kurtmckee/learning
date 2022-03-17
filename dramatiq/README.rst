dramatiq
********

Background
==========

dramatiq is "a background task processing library".

I need to understand how it works so code in this repo follows my learning path.

Requirements are stored in ``requirements.txt``.
I'm using redis as the backend, so the ``[redis]`` extras are enabled for dramatiq.

..  code-block::

    pip install -r requirements.txt


Links
=====

*   `dramatiq <https://dramatiq.io/>`_
*   `redis <https://redis.io/>`_


Experiment 01
=============

Goals
-----

*   Install dramatiq
*   Connect to redis (local instance running at ``localhost:6379``)

Issues
------

*   Installing ``dramatiq[redis]`` wasn't sufficient to complete the intro tutorial.
    It was also necessary to configure dramatiq to use redis as its broker.
    `Bug report submitted <https://github.com/Bogdanp/dramatiq/issues/483>`_

Lessons
-------

*   Running ``dramatiq --watch e01_hello_world`` kicked off the process in the background.
*   It's possible to run the ``count_to()`` as a function.
*   Sending a message to ``count_to()`` using the syntax ``count_to.send(...)`` worked just fine.
