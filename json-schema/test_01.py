import json
import pathlib

import jschon.jsonschema
import jsonschema
import pytest


def run_using_jschon(schema: dict, document: dict, is_valid: bool):
    """Validate a document against a schema using jschon.

    If *is_valid* is False then an error will be anticipated.
    """

    jschon.create_catalog('2020-12')

    json_schema = jschon.JSONSchema(schema)
    json_schema.validate()

    json_document = jschon.JSON(document)
    result = json_schema.evaluate(json_document)
    assert result.output(jschon.jsonschema.OutputFormat.BASIC)["valid"] is is_valid


def run_using_jsonschema(schema: dict, document: dict, is_valid: bool):
    """Validate a document against a schema using jsonschema.

    If *is_valid* is False then an error will be anticipated.
    """

    json_schema = jsonschema.Draft7Validator(schema)
    if is_valid:
        json_schema.validate(document)
    else:
        with pytest.raises(jsonschema.ValidationError):
            json_schema.validate(document)


asl_schema = json.load(pathlib.Path("01-amazon-state-language.schema.json").open())


@pytest.mark.parametrize(
    "filename", pathlib.Path(__file__).parent.glob("01-asl-tests/*.json")
)
@pytest.mark.parametrize("validator", [run_using_jschon, run_using_jsonschema])
def test_files(validator, filename):
    """Test Amazon Step Function files."""

    validator(asl_schema, json.load(filename.open()), "invalid" not in filename.name)
