import pytest

from ai_es_utils.queries.components import LocationQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("location_query.json")


@pytest.mark.parametrize(
    "location, _target_query_body", [
        ("Berlin", target_query_body),
        (None, {})
    ]
)
def test_base_query(location: str, _target_query_body: dict):
    _query = LocationQuery()

    payload = RequestPayload()
    if location is not None:
        payload = RequestPayload(
            query=Query(location="Berlin")
        )

    assert _query.query(payload).query == _target_query_body
