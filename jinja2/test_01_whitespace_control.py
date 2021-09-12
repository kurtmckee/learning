# Test Jinja2 whitespace control for learning purposes.
# Copyright Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT
#
# Jinja2's whitespace control is currently documented here:
# https://jinja.palletsprojects.com/en/3.0.x/templates/#whitespace-control
#

import jinja2
import pytest


@pytest.fixture(scope="function")
def template():
    def setup(
        source,
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    ):
        return jinja2.Template(
            source,
            trim_blocks=trim_blocks,
            lstrip_blocks=lstrip_blocks,
            keep_trailing_newline=keep_trailing_newline,
        )

    return setup


def test_basic(template):
    text = """
        {% if True %}
            #
        {% endif %}
    """

    output = template(text).render()
    assert output.strip() == "#"


@pytest.mark.parametrize(
    "text, expected",
    (
        # Works - no-op
        ("{% if True %}#{% endif %}", "#"),
        # Works - left side
        ("{% if True %}\n#{% endif %}", "#"),
        # Works - right side
        ("{% if True %}#{% endif %}\n", "#"),
        #
        # Spaces break trimming
        ("{% if True %} \n#{% endif %}", " \n#"),
        ("{% if True %}#{% endif %} \n", "# \n"),
    ),
)
def test_trim_blocks(template, text, expected):
    """Test how *trim_blocks* affects rendering."""

    assert template(text, trim_blocks=True).render() == expected


@pytest.mark.parametrize(
    "text, expected",
    (
        # Works - no-op
        ("{% if True %}#{% endif %}", "#"),
        # Works - left side
        (" {% if True %}#{% endif %}", "#"),
        ("\t{% if True %}#{% endif %}", "#"),
        # Works - right side
        ("{% if True %}#\n {% endif %}", "#\n"),
        ("{% if True %}#\n\t{% endif %}", "#\n"),
    ),
)
def test_lstrip_blocks(template, text, expected):
    """Test how *lstrip_blocks* affects rendering."""

    assert template(text, lstrip_blocks=True).render() == expected


@pytest.mark.parametrize(
    "text, expected",
    (
        # Works - no-op
        ("{% if True %}#{% endif %}", "#"),
        # Works
        ("{% if True %}#{% endif %}\n", "#"),
    ),
)
def test_keep_trailing_newline(template, text, expected):
    """Test how *keep_trailing_newline* affects rendering."""

    assert template(text, keep_trailing_newline=False).render() == expected


@pytest.mark.parametrize(
    """text, expected""",
    (
        # Works
        ("{% if True %}#{% endif %}", "#"),
        # Left strips
        (" \r\n\t\v{%- if True %}#{% endif %}", "#"),
        ("{% if True %}# \r\n\t\v{%- endif %}", "#"),
        # Right strips
        ("{% if True -%} \r\n\t\v#{% endif %}", "#"),
        ("{% if True %}#{% endif -%} \r\n\t\v", "#"),
    )
)
def test_explicit_trimming(template, text, expected):
    """Test how in-template whitespace trimming affects rendering."""
    assert template(text).render() == expected
