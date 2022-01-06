import json

import pydantic


class User(pydantic.BaseModel):
    id: pydantic.StrictInt
    name: pydantic.constr(min_length=1, max_length=30, regex=r"[A-Z][a-z]*")
    friends: pydantic.conlist(pydantic.StrictInt) = []


# Instantiate a person.
person_json = {
    "id": 1,
    "name": "Abcd",
}
person = User(**person_json)

assert person != person_json  # The model and the JSON shouldn't match
assert json.loads(person.json()) != person_json  # *friends* is auto-generated
assert json.loads(person.json(exclude_unset=True)) == person_json  # This is approximately correct


try:
    #              v--- str, not int
    User(**{"id": "1", "name": "Abcd"})
except pydantic.ValidationError:
    pass
