import json

import pytest

from e02_json_parsing import parse


@pytest.mark.parametrize(
    "blob, expected_value, expected_type",
    (
        # "Simple" values
        ('""', "", str),
        ("[]", [], list),
        ("{}", {}, dict),
        ("0", 0, int),
        ("0.0", 0.0, float),
        ("true", True, bool),
        ("false", False, bool),
        ("null", None, type(None)),
        # Complex values
        ("[1, 2,3]", [1, 2, 3], list),
        ('{"a": 1, "b": [{"c": true}]}', {"a": 1, "b": [{"c": True}]}, dict),
    )
)
def test_basic_types(blob, expected_value, expected_type):
    result = parse(blob)
    assert result == expected_value
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "blob, exception",
    (
        # Bad JSON
        ("bogus", json.JSONDecodeError),
        # Forbidden constants
        ("Infinity", ValueError),
        ("-Infinity", ValueError),
        ("Nan", ValueError),
        # Duplicate keys
        ('{"key": 1, "key": 2}', KeyError),
        ('{"deep": {"key": 1, "key": 2}}', KeyError),
    )
)
def test_exceptions(blob, exception):
    with pytest.raises(exception):
        parse(blob)
