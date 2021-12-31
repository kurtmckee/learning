JSON schema
###########

What is it?
===========

`JSON schema`_ is a spec for validating JSON documents.
It can be used to specify required keys, types, and values.

I want to understand it better.


How do I use this?
==================

In bash, you can simply run:

..  code-block:: shell

    # Setup the virtual environment.
    python -m venv venv
    . venv/bin/activate
    python -m pip install -U pip setuptools wheel
    python -m pip install -r requirements.txt

    # Run the tests.
    pytest


Files
=====

``01-amazon-state-language.schema.json``
    The `Amazon State Language`_ is used with Amazon Step Functions.
    I decided to write a JSON schema for their spec as a learning opportunity.
    The goal for this file is to do basic validation of any valid Step Function JSON document.

    "Basic" here means that the key, types, and values are correct.
    It is not a goal for this file to ensure that the Step Function logic is correct.


..  URL's
    =====

..  _JSON schema: https://json-schema.org/
..  _Amazon State Language: https://states-language.net/