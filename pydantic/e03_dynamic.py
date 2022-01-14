"""
The goal of this experiment is to list a number of fields exactly once,
create a model using that list, and validate that only exactly one
of the fields is actually passed in.

In addition, I want to learn about validators and sentinel values.
For example, while I need to specify that all fields are optional,
I don't want to accept `None` as a valid value.

The work below implements boolean conditions as documented in the
Amazon State Language specification for Choice states.

Links to current documentation:

* https://pydantic-docs.helpmanual.io/usage/models/#dynamic-model-creation
* https://states-language.net/spec.html
"""

import json
import typing as t

import pydantic as p


# Tuples are not a value type that can be returned when loading JSON documents.
# An Ellipsis cannot be used as a sentinel value because pydantic will believe
# that I mean "This field is required, and its value may be `None`".
SENTINEL = tuple()


MUTUALLY_EXCLUSIVE_BOOLEAN_FIELDS: t.Final[t.Dict] = {
    "And": (t.Optional[t.List["BooleanCondition"]], SENTINEL),
    "Not": (t.Optional["BooleanCondition"], SENTINEL),
    "Or": (t.Optional[t.List["BooleanCondition"]], SENTINEL),
    "Bogus": (t.Literal["Done"], SENTINEL),
}


class Config:
    extra = "forbid"


@p.root_validator
def forbid_multiple_fields(_, values):
    """Only exactly one field may be provided."""

    passed = {k for k, v in values.items() if v is not SENTINEL}
    if len(passed & MUTUALLY_EXCLUSIVE_BOOLEAN_FIELDS.keys()) != 1:
        fields = ", ".join(MUTUALLY_EXCLUSIVE_BOOLEAN_FIELDS)
        raise ValueError(f"Exactly one of {fields} is required and allowed")
    return values


@p.root_validator
def forbid_nulls(_, values):
    """Null values are not permitted."""

    if any(v is None for v in values.values()):
        raise ValueError(f"`null` is not an acceptable value")
    return values


validators = {
    "forbid_multiple_fields": forbid_multiple_fields,
    "forbid_nulls": forbid_nulls,
}


BooleanCondition = p.create_model(
    "BooleanCondition",
    Config=Config,
    __validators__=validators,
    **MUTUALLY_EXCLUSIVE_BOOLEAN_FIELDS,
)


class TopLevelCondition(BooleanCondition):
    """'Next' is a required field at the top level of a condition object."""

    Next: p.constr(min_length=1, max_length=128)


valid_example = {
    "Next": "some-other-state",
    "Not": {
        "Or": [
            {
                "Bogus": "Done",
            },
        ],
    },
}

document = TopLevelCondition(**valid_example)
assert json.loads(document.json(exclude_unset=True)) == valid_example


invalid_examples = [
    # Missing "Next" field.
    {"Bogus": "Done"},

    # "Bogus" field value is incorrect.
    {
        "Next": "state-2",
        "Bogus": "Whatever",
    },
    # "Or" and "And" are mutually exclusive
    {
        "Next": "state-2",
        "And": [{"Bogus": "Done"}],
        "Or": [{"Bogus": "Done"}],
    },
    # "Or" cannot be None, even though it's optional.
    {
        "Next": "state-2",
        "Or": None,
    },
    # No additional keys should ever be allowed (test 1)
    {
        "Next": "some-other-state",
        "Not": {"Bogus": "Done"},
        "Garbage": "Yes",
    },
    # No additional keys should ever be allowed (test 1)
    {
        "Next": "some-other-state",
        "Not": {
            "Bogus": "Done",
            "Garbage": "Yes",
        },
    },
]

for invalid_example in invalid_examples:
    try:
        document = TopLevelCondition(**invalid_example)
    except p.ValidationError as error:
        pass
    else:
        print("-" * 20)
        print(invalid_example)
        raise ValueError("pydantic did not complain!")


# Conclusion:
#
# * Dynamic creation seems to work well
# * An Ellipsis (`...`) CANNOT be used as a sentinel default value
# * Dealing with mutually-exclusive fields requires:
#   * Specifying that every field is optional
#     (so the field doesn't HAVE to be specified)
#   * Verifying that `None` values are excluded
#     (since optional fields can accept `None` as a valid value)
#
