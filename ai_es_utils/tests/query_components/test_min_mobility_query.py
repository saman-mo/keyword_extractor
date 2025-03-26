import pytest

from ai_es_utils.queries.components import MinMobilityQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("min_mobility_query.json")


@pytest.mark.parametrize(
    "mobility, _target_query_body", [
        (10, target_query_body),
        (None, {})
    ]
)
def test_base_query(mobility: int, _target_query_body: dict):
    _query = MinMobilityQuery()

    payload = RequestPayload()
    if mobility is not None:
        payload = RequestPayload(
            query=Query(mobility=mobility)
        )

    assert _query.query(payload).query == _target_query_body
