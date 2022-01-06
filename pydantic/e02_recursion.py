"""
This is a test of Pydantic's ability to parse recursive data.

In particular, I'm investigating how it might handle Amazon's state language.
For example, Choice states have very simple rules that might still be tough
to implement.
"""

import enum
import json
from typing import Dict, List, Optional

import pydantic

json_document = {
    "StartAt": "State1",
    "States": {
        "State1": {
            "Type": "Choice",
            "Choices": [
                {
                    "Next": "StateEnd",
                    "Variable": "$.key",
                    "StringEquals": "some-expected-value",
                },
                {
                    "Next": "StateEnd",
                    "Not": {
                        "Or": [
                            {
                                "Variable": "$.inconsistent",
                                "IsPresent": True,
                            },
                            {
                                "Variable": "$.inconsistent",
                                "StringNotEquals": "some-other-value",
                            },
                        ],
                    },
                },
            ],
        },
        "StateEnd": {
            "Type": "Pass",
            "End": True,
        },
    },
}


class Comparison(pydantic.BaseModel):
    Variable: Optional[pydantic.constr(regex=r"\$\..+")]
    StringEquals: Optional[pydantic.StrictStr]
    StringNotEquals: Optional[pydantic.StrictStr]
    IsPresent: Optional[pydantic.StrictBool]
    Not: Optional['Comparison']
    Or: Optional[List['Comparison']]


class TopComparison(Comparison):
    # Only the top-level comparison can have a "Next" field.
    Next: pydantic.StrictStr


class StateTypeEnum(str, enum.Enum):
    Pass = "Pass"
    Choice = "Choice"


class IndividualState(pydantic.BaseModel):
    Type: StateTypeEnum
    Choices: Optional[List[TopComparison]]
    End: Optional[bool]


class StateLanguage(pydantic.BaseModel):
    StartAt: pydantic.constr(strict=True, min_length=1, max_length=128)
    States: Dict[str, IndividualState]


document = StateLanguage(**json_document)

assert json.loads(document.json(exclude_unset=True)) == json_document


# Conclusions thus far:
#
# * Recursion seems to work well.
# * I need to test validation for mutually-exclusive elements.
#
