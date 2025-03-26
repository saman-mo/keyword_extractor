import json
import os

import pytest
from pydantic import ValidationError

from ai_es_utils.queries.models.payload import ValidatedPayload
from .utils import add_pytest_cwd


def load_payload(file_name: str) -> dict:
    return json.load(open(add_pytest_cwd(os.path.join("test_data", "request_payloads", file_name))))


def test_parsing_query_with_all_filters():
    payload = load_payload("payload_all_filters.json")
    ValidatedPayload(**payload)


@pytest.mark.parametrize(
    "request_payload, should_raise", [
        ({"query": {"jobTitle": "java developer", "includePortals": ["xing"]}}, False),
        ({"query": {"jobTitle": "java developer", "excludePortals": ["xing"]}}, False),
        ({"query": {"jobTitle": "java developer", "includePortals": ["xing"], "excludePortals": ["linkedin"]}},
         True),
        ({"query": {"jobTitle": "java developer", "worksAt": ["Google"]}}, False),
        ({"query": {"jobTitle": "java developer", "worksAtExclude": ["Apple"]}}, False),
        ({"query": {"jobTitle": "java developer", "worksAt": ["Google"], "worksAtExclude": ["Apple"]}}, True),
        ({"query": {"jobTitle": "java developer", "previouslyAt": ["Google"]}}, False),
        ({"query": {"jobTitle": "java developer", "previouslyAtExclude": ["Yahoo"]}}, False),
        ({"query": {"jobTitle": "java developer", "previouslyAt": ["Google"], "previouslyAtExclude": ["Yahoo"]}},
         True)
    ]
)
def test_portals_filter_are_mutually_exclusive(request_payload, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            ValidatedPayload(**request_payload)
    else:
        ValidatedPayload(**request_payload)


@pytest.mark.parametrize(
    "payload", [
        ({"query": {"jobTitle": 4}}),
        ({"query": {"skills": "machine learning"}}),
        ({"query": {"jobTitle": "java developer", "previouslyAt": "Yahoo"}}),
        ({"query": {"jobTitle": "java developer", "freelancerOnly": 4}}),
        ({"query": {"jobTitle": "java developer", "location": "Hamburg", "distance": 0}}),
        ({"query": {"jobTitle": "java developer", "location": "Berlin", "distance": -1}}),
    ]
)
def test_raising_error_for_invalid_input(payload):
    with pytest.raises(ValidationError):
        ValidatedPayload(**payload)


@pytest.mark.parametrize(
    "payload", [
        ({"query": {"jobTitle": "java developer", "distance": 0}}),
        ({"query": {"jobTitle": "java developer", "distance": -1}}),
    ]
)
def test_valid_input(payload):
    try:
        ValidatedPayload(**payload)
    except ValidationError:
        pytest.fail("Raised validation error on valid query!")
