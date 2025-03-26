import pytest

from ai_es_utils.queries.components import MinChangeProbabilityQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("min_change_probability_query.json")


@pytest.mark.parametrize(
    "change_probability, _target_query_body", [
        (99, target_query_body),
        (None, {})
    ]
)
def test_base_query(change_probability: int, _target_query_body: dict):
    _query = MinChangeProbabilityQuery()

    payload = RequestPayload()
    if change_probability is not None:
        payload = RequestPayload(
            query=Query(changeProbability=change_probability)
        )

    assert _query.query(payload).query == _target_query_body
