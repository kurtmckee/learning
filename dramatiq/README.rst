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


Running these experiments generally looks like this:

..  code-block:: sh

    # Launch the workers...DO NOT include '.py' in the filename!
    # The `--watch .` apparently tells dramatiq to watch for file changes.
    dramatiq --watch . e02_error_handling

    # Send a message
    python e02_error_handling handled 3
    python e02_error_handling handled 17
    python e02_error_handling unhandled 17


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


Experiment 02
=============

Goals
-----

*   Understand error handling

Lessons
-------

*   The tutorial's version of error handling is just a ``try/except`` block.

Questions
---------

*   Q: If a task must be retried, does the dramatiq worker sleep (and is thus unavailable from that point on)?

    *   A: Looks like workers don't sleep and retry themselves.

        The log output shows that ``Thread-6`` processed the task the first time,
        ``Thread-11`` processed the task the second time, followed by ``Thread-8``.

        The dramatiq docs also use the phrase "automatically enqueues a retry":

            Dramatiq assumes all actors are idempotent so when an exception occurs during message processing,
            it automatically enqueues a retry for that message with exponential backoff.

*   Q: If the worker isn't sleeping, does that mean a task can be scheduled to be re-run at a specific time?

    *   A: Not exactly for a specific time, but it's possible to specify a delay.

        The dramatiq docs state that the ``send_with_options()`` method accepts a ``delay`` keyword argument in milliseconds.


Experiment 03
=============

Goals
-----

*   Reduce the number of dramatiq workers (hopefully down to 1!)
*   Prioritize some tasks over others.
*   Verify that when resources are limited, workers choose prioritized tasks.

To run it
---------

I ran dramatiq using this command:

..  code-block:: sh

    dramatiq --watch . e03_priorities

I then kicked off 100 sleeps and 1 prioritized greeting:

..  code-block:: sh

    python e03_priorities.py auto

Later I discovered how to configure process and thread counts, so I retested with:

..  code-block:: sh

    # Shell 1
    dramatiq --watch . --processes 1 --threads 1 e03_priorities

    # Shell 2
    python e03_priorities.py auto

The expected output was "Sleeping", followed immediately by a "Hello!", followed by more sleeps.
However, I didn't see that happen.

Lessons
-------

*   Priorities are set per *actor*, not per *message*.
    I thought messages could have individualized priorities but that's not the case.
*   Use priority constants (like ``HIGH_PRIORITY``), rather than integer literals (like ``0``).
*   Priorities DO NOT mean that something will instantly jump ahead in the queue.
    The dramatiq docs suggest that priorities might only be tie-breakers for things scheduled at the exact same time:

        When choosing between two concurrent messages to run,
        Dramatiq will run the Message that belongs to the actor with the highest priority.

Questions
---------

*   Q: It looks like dramatiq kicks off 16 processes by default, and I only see "Thread-4" through "Thread-11" in the output.
    Does dramatiq default to 16 processes and 8 threads per process?

    *   A: It doesn't seem to exist in the docs, but the CLI shows, yes, 16 processes with 8 threads each.

*   Q: How do I configure the number of processes?

    *   A: ``dramatiq --processes x ...``.

*   Q: How do I configure the number of threads?

    *   A: ``dramatiq --threads y ...``.
