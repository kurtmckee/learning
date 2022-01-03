import json
from typing import Any, Dict, List, Tuple


def forbid_constants(constant: str):
    """Forbid "-Infinity", "Infinity", and "NaN" constants.

    By default, the `json` module supports infinity and NaN as float constants.
    These constants are not part of the JSON specification.

    :raises ValueError:
        ``ValueError`` is always raised when this function is called.

    """

    raise ValueError(f"Forbidden constant detected: {constant}")


def forbid_duplicate_keys(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    """Parse JSON objects but forbid duplicate keys.

    By default, the `json` module quietly swallows duplicate object keys.
    This function prevents this from happening.

    :raises KeyError:
        If duplicate keys are detected then KeyError will be raised.

    """

    result = {}
    for key, value in pairs:
        if key in result:
            raise KeyError(f"Duplicate key detected: {key}")
        result[key] = value
    return result


def parse(blob: str):
    """Parse JSON with stricter requirements.

    * Invalid JSON raise ``json.JSONDecodeError``.
    * Duplicate object keys raise ``KeyError``.
    * Infinity and NaN constants raise ``ValueError``.
    """

    try:
        return json.loads(
            blob,
            object_pairs_hook=forbid_duplicate_keys,
            parse_constant=forbid_constants,
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        # Enumerate known exceptions for visibility.
        raise
